import datetime
import json
import logging
import re
import time
import uuid

import pika

from queue import Queue
from collections import deque
import threading

import sys
import signal

try:
    import configparser as config_parser  # py3
except ImportError:
    import ConfigParser as config_parser  # py2

log = logging.getLogger("org.openbaton.python.vnfm.sdk.%s" % __name__)
registration_response = registration_corr_id = None


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


def start_vim_driver(vim_driver_class, config_file, number_maximum_worker_threads, number_listener_threads,
                     number_reply_threads, vim_driver_type, vim_driver_name):
    log.debug("Config file location: %s" % config_file)
    config = config_parser.ConfigParser()
    config.read(config_file)
    props = get_map(section='vim', config=config)
    rabbit_uname = props.get('username')
    rabbit_pwd = props.get('password')
    broker_ip = props.get('broker_ip', '127.0.0.1')
    rabbit_port = props.get('port', 5672)
    heartbeat = int(props.get('heartbeat', 60))
    exchange_name = props.get('exchange-name', 'openbaton-exchange')

    vim_driver_uname, vim_driver_pwd = register_vim_driver(broker_ip, rabbit_port, rabbit_uname, rabbit_pwd,
                                                           exchange_name, heartbeat, vim_driver_type)
    rabbit_credentials = pika.PlainCredentials(vim_driver_uname, vim_driver_pwd)

    reply_queue = Queue()
    stop_event = threading.Event()
    worker_pool = WorkerPool(reply_queue, vim_driver_class, number_maximum_worker_threads)
    listener_threads = [ListenerThread(vim_driver_class, worker_pool, broker_ip, rabbit_port, heartbeat, exchange_name,
                                       rabbit_credentials, vim_driver_type, vim_driver_name) for _ in
                        range(number_listener_threads)]
    reply_threads = [ReplyThread(broker_ip, rabbit_port, rabbit_credentials, exchange_name,
                                 heartbeat, reply_queue) for _ in range(number_reply_threads)]
    stop_signal_handler = StopSignalHandler(stop_event)
    signal.signal(signal.SIGINT, stop_signal_handler)

    for t in listener_threads:
        t.start()
    log.debug('Started listener threads')

    for t in reply_threads:
        t.start()
    log.debug('Started reply threads')

    stop_event.wait()
    print('Shutting down...')

    for t in listener_threads:
        t.stop()

    for t in listener_threads:
        t.join()

    log.debug('Listener threads stopped')

    worker_pool.shutdown()

    log.debug('Worker threads stopped')

    reply_queue.join()

    for t in reply_threads:
        t.stop_running = True

    for _ in range(number_reply_threads):
        reply_queue.put((None, None, None))

    for t in reply_threads:
        t.join()
    log.debug('Reply threads stopped')


class NoWorkerAvailable(Exception):
    pass


class WorkerPool():
    def __init__(self, reply_queue, vim_driver_class, max_threads=0, *vim_driver_args):
        self.reply_queue = reply_queue
        self.threads = []
        self.lock = threading.Lock()
        self.max_threads = max_threads
        self.pool_not_full = threading.Event()
        self.stopped = False
        self.vim_driver_args = vim_driver_args
        self.vimdriver_class = vim_driver_class

    def submit_message(self, message):
        with self.lock:
            if self.stopped:
                raise Exception('WorkerPool has already been stopped')
            if self.max_threads == 0 or len(self.threads) < self.max_threads:
                vim_driver_instance = self.vimdriver_class(*self.vim_driver_args)
                new_thread = WorkerThread(self.remove_thread, self.reply_queue, vim_driver_instance.process_message,
                                          message)
                new_thread.start()
                self.threads.append(new_thread)
            else:
                raise NoWorkerAvailable()

    def remove_thread(self, thread):
        with self.lock:
            if not self.stopped:
                self.threads.remove(thread)

    def shutdown(self):
        with self.lock:
            self.stopped = True
        for t in self.threads:
            t.join()


class WorkerThread(threading.Thread):
    def __init__(self, remove_thread_callback, reply_queue, process_message_function, message):
        super(WorkerThread, self).__init__()
        self.remove_thread_callback = remove_thread_callback
        self.reply_queue = reply_queue
        self.process_message_function = process_message_function
        self.message = message

    def run(self):
        response = None
        try:
            channel, method, props, body = self.message
            response = self.process_message_function(body)
        finally:
            if response is not None:
                self.reply_queue.put((props.reply_to, props.correlation_id, response))
            self.remove_thread_callback(self)


def register_vim_driver(broker_ip, rabbit_port, rabbit_uname, rabbit_pwd, exchange_name, heartbeat, vim_driver_type):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=broker_ip,
                                                                   port=rabbit_port,
                                                                   credentials=pika.PlainCredentials(rabbit_uname,
                                                                                                     rabbit_pwd),
                                                                   heartbeat_interval=heartbeat))

    channel = connection.channel()
    channel.exchange_declare(exchange=exchange_name, passive=True)
    channel.basic_qos(prefetch_count=1)

    result = channel.queue_declare(exclusive=True)
    callback_queue = result.method.queue

    def _on_response(ch, method, props, body):
        global registration_response, registration_corr_id
        if registration_corr_id == props.correlation_id:
            registration_response = body

    channel.basic_consume(_on_response, no_ack=True, queue=callback_queue)
    global registration_response, registration_corr_id
    registration_corr_id = str(uuid.uuid4())
    register_message = json.dumps(dict(type=vim_driver_type,
                                       action='register'))
    for i in range(1800):
        if i % 100 == 0:
            log.debug("Sending registration message %s" % register_message)
            channel.basic_publish(exchange=exchange_name,
                                  routing_key='nfvo.manager.handling',
                                  properties=pika.BasicProperties(
                                      reply_to=callback_queue,
                                      correlation_id=registration_corr_id,
                                      content_type='text/plain'
                                  ),
                                  body=register_message)
        connection.process_data_events()
        if registration_response is not None:
            break
        time.sleep(0.1)
    else:
        log.error('After 180 seconds no registration response was received. Giving up...')
        channel.close()
        connection.close()
        sys.exit(1)

    if isinstance(registration_response, bytes):
        registration_response = registration_response.decode("utf-8")

    response_dict = json.loads(registration_response)
    channel.queue_delete(queue=callback_queue)
    return response_dict.get('rabbitUsername'), response_dict.get('rabbitPassword')


def connect_to_rabbitmq(broker_ip, rabbit_port, rabbit_credentials, exchange_name, queue_name):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=broker_ip,
                                                                   port=rabbit_port,
                                                                   credentials=rabbit_credentials))
    channel = connection.channel()
    channel.exchange_declare(exchange=exchange_name, passive=True)
    channel.basic_qos(prefetch_count=1)

    if queue_name is not None:
        channel.queue_declare(queue_name, passive=True)
    return connection, channel


def deregister_vim_driver(broker_ip, rabbit_port, vim_driver_uname, vim_driver_pwd, exchange_name):
    try:

        connection, channel = connect_to_rabbitmq(broker_ip, rabbit_port,
                                                  pika.PlainCredentials(vim_driver_uname, vim_driver_pwd),
                                                  exchange_name, 'nfvo.manager.handling')
        deregister_message = json.dumps(dict(username=vim_driver_uname,
                                             password=vim_driver_pwd,
                                             action='unregister'))

        channel.basic_publish(exchange=exchange_name,
                              routing_key='nfvo.manager.handling',
                              properties=pika.BasicProperties(
                                  content_type='text/plain'
                              ),
                              body=deregister_message)

    except Exception as e:
        log.debug('Exception while deregistering VIM Driver: {}'.format(e))
    channel.close()
    connection.close()


class ListenerThread(threading.Thread):
    """This class fetches new messages from the vim-drivers.<type>.<name> RabbitMQ queue
    and dispatches them to the worker threads for processing them.
    If all the permanent worker threads are busy it will create a new thread if the maximum number
    of threads is not yet reached. If the new thread is not needed anymore after it has finished
    processing the message it will be removed again."""

    def __init__(self, vim_driver_class, worker_pool, broker_ip, rabbit_port, heartbeat, exchange_name,
                 rabbit_credentials, vim_driver_type, vim_driver_name=None, *vim_driver_args):
        super(ListenerThread, self).__init__()
        self.vim_driver_type = vim_driver_type
        self.vim_driver_name = vim_driver_name if vim_driver_name is not None else vim_driver_type
        self.queue_name = "vim-drivers.%s.%s" % (self.vim_driver_type, self.vim_driver_name)
        self.worker_pool = worker_pool

        self.rabbit_credentials = rabbit_credentials
        self.heartbeat = heartbeat
        self.broker_ip = broker_ip
        self.rabbit_port = rabbit_port
        self.exchange_name = exchange_name
        self.connection = None
        self.channel = None
        self.vim_driver_class = vim_driver_class
        self.vim_driver_args = vim_driver_args

    def run(self):
        """Start the message dispatcher."""
        log.debug("Connecting to %s" % self.broker_ip)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.broker_ip, credentials=self.rabbit_credentials,
                                      heartbeat_interval=self.heartbeat))

        self.channel = self.connection.channel()
        self.channel.basic_qos(prefetch_count=1)

        self.channel.queue_declare(queue=self.queue_name, durable=True, auto_delete=True)
        self.channel.queue_bind(exchange=self.exchange_name, queue=self.queue_name, routing_key=self.queue_name)
        self.channel.basic_consume(self.dispatch, no_ack=False, queue=self.queue_name)

        try:
            self.channel.start_consuming()
        except OSError as e:
            log.debug(
                'Ignoring OSError which occurs sometimes during shut down and is probably a bug in pika: {}'.format(e))

    def stop(self):
        """Stop listening for messages."""
        self.channel.stop_consuming()
        self.channel.close()
        self.connection.close()

    def dispatch(self, ch, method, props, body):
        log.debug('Dispatching message')
        self.channel.basic_ack(delivery_tag=method.delivery_tag)
        while True:
            try:
                self.worker_pool.submit_message((ch, method, props, body))
                break
            except NoWorkerAvailable:
                time.sleep(0.2)
        log.debug('Message dispatched')


class ReplyThread(threading.Thread):
    def __init__(self, broker_ip, rabbit_port, rabbit_credentials, exchange_name, heartbeat, reply_queue):
        super(ReplyThread, self).__init__()
        self.broker_ip = broker_ip
        self.rabbit_port = rabbit_port
        self.rabbit_credentials = rabbit_credentials
        self.exchange_name = exchange_name
        self.connection, self.channel = connect_to_rabbitmq(broker_ip, rabbit_port, rabbit_credentials,
                                                            exchange_name, None)
        # self.channel.queue_declare(queue=queue_name, durable=True, auto_delete=True, passive=True)
        self.reply_queue = reply_queue
        self.stop_running = False

    def run(self):
        try:
            while not self.stop_running:
                reply_to, corr_id, response = self.reply_queue.get()
                if self.stop_running:
                    self.reply_queue.task_done()
                    break
                try:
                    self.channel.basic_publish(exchange=self.exchange_name, routing_key=reply_to,
                                               properties=pika.BasicProperties(correlation_id=corr_id,
                                                                               content_type='text/plain'),
                                               body=response)
                except pika.exceptions.ConnectionClosed:
                    log.warning('Pika connection closed. Heartbeat is probably too low. \
                                    Trying to connect and send message again.')
                    self.connection, self.channel = connect_to_rabbitmq(self.broker_ip, self.rabbit_port,
                                                                        self.rabbit_credentials,
                                                                        self.exchange_name, None)
                    self.channel.basic_publish(exchange=self.exchange_name, routing_key=reply_to,
                                               properties=pika.BasicProperties(correlation_id=corr_id,
                                                                               content_type='text/plain'),
                                               body=response)
                finally:
                    self.reply_queue.task_done()

                log.info("Answer sent")
        finally:
            try:
                self.channel.close()
                self.connection.close()
            except pika.exceptions.ConnectionClosed:
                log.warning('Connection of reply thread is already closed.')


class StopSignalHandler():
    def __init__(self, stop_event):
        self.stop_event = stop_event
        self.already_stopping = False

    def __call__(self, signum, frame):
        if not self.already_stopping:
            self.already_stopping = True
            self.stop_event.set()
        else:
            sys.exit()

