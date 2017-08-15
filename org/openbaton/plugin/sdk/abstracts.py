import json
import logging
import os
import threading
import traceback
from datetime import date

import pika

from org.openbaton.plugin.sdk.utils import convert_from_camel_to_snake

try:
    import configparser as config_parser  # py3
except ImportError:
    import ConfigParser as config_parser  # py2

log = logging.getLogger("org.openbaton.plguin.vim.sdk.%s" % __name__)


class AbstractPluginHelper(threading.Thread):
    #  This version must match the version of the plugin...
    def __init__(self, _type, properties, username, password, plugin_name=None):
        if not plugin_name:
            plugin_name = _type

        self.plugin_name = plugin_name

        super(AbstractPluginHelper, self).__init__()

        self.queuedel = True
        self._stop_running = False
        log.addHandler(logging.NullHandler())
        self.type = _type

        self.properties = properties

        logging_dir = self.properties.get('log_path')

        if not os.path.exists(logging_dir):
            os.makedirs(logging_dir)

        file_handler = logging.FileHandler("{0}/{1}-plugin.log".format(logging_dir, self.type))
        file_handler.setLevel(level=logging.DEBUG)
        log.addHandler(file_handler)

        self.heartbeat = self.properties.get("heartbeat", "60")
        self.exchange_name = self.properties.get("exchange", 'openbaton-exchange')
        self.durable = self.properties.get("exchange_durable", True)
        self.queue_name = "vim-drivers.%s.%s" % (self.type, self.plugin_name)

        self.rabbit_credentials = pika.PlainCredentials(username, password)
        self.channel = None

    def __on_request__(self, ch, method, props, body):
        response = self.__on_message__(body)
        # log.debug("Answer is \n\n%s" % response)
        ch.basic_ack(delivery_tag=method.delivery_tag)

        if response:
            ch.basic_publish(exchange='',
                             routing_key=props.reply_to,
                             properties=pika.BasicProperties(correlation_id=props.correlation_id,
                                                             content_type='text/plain'),
                             body=response)
            # ch.basic_ack(delivery_tag=method.delivery_tag)
            log.info("Answer sent")

    def __on_message__(self, body):
        if isinstance(body, bytes):
            body = body.decode("utf-8")
        message = json.loads(body)
        params = message.get('parameters')
        method_name = convert_from_camel_to_snake(message.get('methodName'))
        log.debug("Looking for method %s" % method_name)

        method = getattr(self, method_name)
        answer = {}
        try:
            ret_obj = method(*params)
            if not ret_obj:
                return ret_obj
            if not isinstance(ret_obj, dict) and not isinstance(ret_obj, list):
                answer['answer'] = ret_obj.get_dict()
            elif isinstance(ret_obj, list):
                answer['answer'] = []
                for obj in ret_obj:
                    if type(obj) in (int, float, bool, str, date, dict):
                        answer['answer'] = ret_obj
                        break
                    else:
                        json_obj = obj.get_dict()
                        answer['answer'].append(json_obj)
            else:
                answer['answer'] = ret_obj

        except:
            traceback.print_exc()
            answer['exception'] = traceback._cause_message
        return json.dumps(answer)

    def _set_stop(self):
        self.channel.stop_consuming()

    def __thread_function__(self, ch, method, properties, body):
        threading.Thread(target=self.__on_request__, args=(ch, method, properties, body)).start()

    def run(self):
        log.debug("Connecting to %s" % self.properties.get("broker_ip"))
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.properties.get("broker_ip"), credentials=self.rabbit_credentials,
                                      heartbeat_interval=int(self.heartbeat)))

        self.channel = connection.channel()
        self.channel.basic_qos(prefetch_count=1)

        self.channel.queue_declare(queue=self.queue_name,
                                   auto_delete=self.queuedel,
                                   durable=self.durable)
        self.channel.queue_bind(exchange=self.exchange_name, queue=self.queue_name)
        self.channel.basic_consume(self.__thread_function__, no_ack=False, queue=self.queue_name)

        log.info("Waiting for actions")

        # Pika is bugged
        # self.channel.start_consuming()
        while self.channel._consumer_infos:
            self.channel.connection.process_data_events(time_limit=1)
