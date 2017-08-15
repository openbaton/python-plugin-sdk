import json
import logging
import re
import time
import uuid

import pika

try:
    import configparser as config_parser  # py3
except ImportError:
    import ConfigParser as config_parser  # py2

log = logging.getLogger("org.openbaton.python.vnfm.sdk.%s" % __name__)
response = corr_id = None


def get_map(section, config):
    dict1 = {}
    options = config.options(section)
    for option in options:
        try:
            dict1[option] = config.get(section, option)
            if dict1[option] == -1:
                log.debug(("skip: %s" % option))
        except:
            log.debug(("exception on %s!" % option))
            dict1[option] = None
    return dict1


def convert_from_camel_to_snake(string):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', string)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def start_plugin_instances(plugin_class, _type, config_file, instances=1, plugin_name=None):
    """
    This utility method start :instances number of thread of class vnfm_klass.

    :param plugin_class: the Class of the Plugin
    :param _type: the type of the Plugin
    :param config_file: the configuration file of the Plugin
    :param instances: the number of instances

    """
    # Configuration file initialisation
    log.debug("Config file location: %s" % config_file)
    config = config_parser.ConfigParser()
    config.read(config_file)
    props = get_map(section='vim', config=config)
    plugin_username, plugin_password = get_rabbit_plugin_credentials(_type=_type,
                                                                     broker_ip=props.get("broker_ip", "127.0.0.1"),
                                                                     port=int(props.get("port", 5672)),
                                                                     username=props.get("username"),
                                                                     password=props.get("password"),
                                                                     heartbeat=props.get("heartbeat", 60),
                                                                     exchange_name=props.get("exchange-name",
                                                                                             "openbaton-exchange"))
    plugin = plugin_class(_type, props, plugin_username, plugin_password, plugin_name)
    log.debug("Plugin Class: %s" % plugin_class)
    threads = []
    plugin.start()
    threads.append(plugin)

    for index in range(1, instances):
        instance = plugin_class(_type, props, plugin_username, plugin_password, plugin_name)
        instance.start()
        threads.append(instance)

    while len(threads) > 0:
        new_threads = []
        try:
            for t in threads:
                if t is not None and t.isAlive():
                    t.join(1)
                    new_threads.append(t)
            threads = new_threads
        except KeyboardInterrupt:
            log.info("Ctrl-c received! Sending kill to threads...")
            for t in threads:
                t._set_stop()
            plugin._set_stop()

    unregister_plugin(
        broker_ip=props.get("broker_ip", "127.0.0.1"),
        port=int(props.get("port", 5672)),
        username=plugin_username,
        password=plugin_password,
        heartbeat=props.get("heartbeat", 60),
        exchange_name=props.get("exchange-name",
                                "openbaton-exchange"))


def get_rabbit_plugin_credentials(_type, broker_ip="localhost", port=5672, username=None, password=None, heartbeat=60,
                                  exchange_name="openbaton-exchange"):
    global response, corr_id
    rabbit_credentials = pika.PlainCredentials(username=username, password=password)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=broker_ip,
                                                                   port=port,
                                                                   credentials=rabbit_credentials,
                                                                   heartbeat_interval=int(heartbeat)))

    channel = connection.channel()

    result = channel.queue_declare(exclusive=True)
    callback_queue = result.method.queue

    def _on_response(ch, method, props, body):
        global response, corr_id
        if corr_id == props.correlation_id:
            response = body

    channel.basic_consume(_on_response, no_ack=True, queue=callback_queue)
    response = None
    corr_id = str(uuid.uuid4())
    register_message = json.dumps(dict(type=_type,
                                       action="register"))
    log.debug("Sending register message %s" % register_message)
    channel.basic_publish(exchange=exchange_name,
                          routing_key='nfvo.manager.handling',
                          properties=pika.BasicProperties(
                              reply_to=callback_queue,
                              correlation_id=corr_id,
                          ),
                          body=register_message)
    while response is None:
        connection.process_data_events()
        time.sleep(0.1)

    if isinstance(response, bytes):
        response = response.decode("utf-8")

    response_dict = json.loads(response)
    channel.queue_delete(queue=callback_queue)
    return response_dict.get('rabbitUsername'), response_dict.get('rabbitPassword')


def unregister_plugin(username, password, broker_ip="localhost", port=5672, heartbeat=60,
                      exchange_name="openbaton-exchange"):
    rabbit_credentials = pika.PlainCredentials(username=username, password=password)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=broker_ip,
                                                                   port=port,
                                                                   credentials=rabbit_credentials,
                                                                   heartbeat_interval=int(heartbeat)))

    channel = connection.channel()
    unregister_message = json.dumps(dict(username=username,
                                         password=password,
                                         action="unregister"))
    channel.basic_publish(
        exchange=exchange_name,
        routing_key='nfvo.manager.handling',
        body=unregister_message
    )


def get_manager_endpoint(_type, description, endpoint):
    return dict(type=_type,
                endpoint=endpoint or _type,
                endpointType="RABBIT",
                description=description,
                enabled=True,
                active=True)
