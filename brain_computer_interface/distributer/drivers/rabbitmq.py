import json

import furl
import pika
from pika.exceptions import AMQPConnectionError


class RabbitMQScheme:
    scheme = 'rabbitmq'

    def __init__(self, url: furl.furl):
        self.host = url.host
        self.port = url.port

    def connect(self):
        try:
            if not self.host or not isinstance(self.host, str) \
               or not self.port or not isinstance(self.port, int):
                raise AMQPConnectionError()
            self.conn = pika.BlockingConnection(
                pika.ConnectionParameters(host=self.host, port=self.port,
                                          connection_attempts=3,
                                          retry_delay=5))
        except AMQPConnectionError as error:
            addr = f'{self.host}:{self.port}'
            err_msg = f'Failed to connect - bad values were given {addr}'
            raise ValueError(err_msg) from error

    def publish_raw_snapshot(self, data):
        # It is advised to have only one channel per thread
        # and currently, publish_raw_snapshot is called per thread.
        channel = self.conn.channel()
        # Creating queues is idempotent.
        # If the queue is yet to be created we will receive an error.
        # Hence we declare (create) anyway.
        # declaring the queue as durable protects the queue from mq restarts
        channel.queue_declare(queue='snapshot', durable=True)
        # Declaring persistent protects the message from mq restarts
        channel.basic_publish(exchange='', routing_key='snapshot',
                              body=json.dumps(data),
                              properties=pika.BasicProperties(
                                  delivery_mode=pika.DeliveryMode.Persistent))
        channel.close()

    def subscribe(self, callback):
        # It is advised to have only one channel per consumer
        # and currently, subscribe is called per consumer.
        channel = self.conn.channel()
        # Creating queues is idempotent.
        # If the queue is yet to be created we will receive an error.
        # Hence we declare (create) anyway.
        # declaring the queue as durable protects the queue from mq restarts
        channel.queue_declare(queue='snapshot', durable=True)
        # This setting make sure not to give more than one message to a worker at a time.
        # Or, in other words, don't dispatch a new message to a worker until it has
        # processed and acknowledged the previous one.
        # Not specifying this will results in round robbin - dispatch evenly.
        channel.basic_qos(prefetch_count=1)
        def _callback(ch, method, properties, body):
            callback(json.loads(body))
            # sends ack when done, if an ack was not sent the message will be resent
            ch.basic_ack(delivery_tag=method.delivery_tag)
        channel.basic_consume(
            queue='snapshot', on_message_callback=_callback)
        try:
            channel.start_consuming()
        except SystemExit:
            channel.close()

    def close(self):
        self.conn.close()
