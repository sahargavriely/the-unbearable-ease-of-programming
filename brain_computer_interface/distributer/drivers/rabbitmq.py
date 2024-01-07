import contextlib
import json
from typing import Iterator

import furl
from pika import (
    BasicProperties,
    BlockingConnection,
    ConnectionParameters,
    DeliveryMode,
)
from pika.exceptions import AMQPConnectionError
from pika.adapters.blocking_connection import BlockingChannel


class RabbitMQScheme:
    # We can also implement the same thing using `routing_key` and
    # `binding_key` as exchanges and set their topic to `fanout`.
    # Moving from one exchange to multiple, emitting the routing complexity.
    scheme = 'rabbitmq'
    exchange = 'one'

    def __init__(self, url: furl.furl):
        self.host = url.host
        self.port = url.port

    def connect(self):
        try:
            if not self.host or not isinstance(self.host, str) \
               or not self.port or not isinstance(self.port, int):
                raise AMQPConnectionError()
            self.conn = BlockingConnection(
                ConnectionParameters(host=self.host, port=self.port,
                                     connection_attempts=8, retry_delay=2))
        except AMQPConnectionError as error:
            addr = f'{self.host}:{self.port}'
            err_msg = f'Failed to connect - bad values were given {addr}'
            raise ValueError(err_msg) from error

    def close(self):
        self.conn.close()

    def publish(self, data, routing_key):
        with _topic_exchange_channel(self.conn, self.exchange) as channel:
            # Declaring persistent protects the message from mq restarts
            channel.basic_publish(exchange=self.exchange,
                                  routing_key=routing_key,
                                  body=json.dumps(data),
                                  properties=BasicProperties(
                                      delivery_mode=DeliveryMode.Persistent))

    def subscribe(self, callback, binding_key, subscriber_group=''):
        with _topic_exchange_channel(self.conn, self.exchange) as channel:
            # Declaring durable protects from mq restarts
            # Declaring exclusive deletes it once the connection closes
            # But we don't want to delete a queue if it's part of a group
            result = channel.queue_declare(queue=subscriber_group,
                                           durable=True,
                                           exclusive=not subscriber_group)
            queue_name = result.method.queue
            channel.queue_bind(exchange=self.exchange, routing_key=binding_key,
                               queue=queue_name)
            # Makes sure not to give more than one msg to a worker at a time.
            # In other words, don't dispatch a new msg to a worker,
            # from the queue, until it has acknowledged the previous one.
            # Removal will results in round robbin - evenly dispatch.
            channel.basic_qos(prefetch_count=1)

            def _callback(ch, method, properties, body):
                callback(json.loads(body))
                # Ack when done, if an ack wasn't send the msg will be resent
                ch.basic_ack(delivery_tag=method.delivery_tag)

            channel.basic_consume(
                queue=queue_name, on_message_callback=_callback)
            channel.start_consuming()


@contextlib.contextmanager
def _topic_exchange_channel(conn: BlockingConnection, exchange) \
        -> Iterator[BlockingChannel]:
    # It is advised to have only one channel per thread
    # and currently, publish_raw_snapshot is called per thread.
    channel = conn.channel()
    # Creating queues/exchanges is idempotent.
    # If the queue/exchange is yet to be created we will receive an error.
    # Hence we declare (create) anyway.
    channel.exchange_declare(exchange=exchange, exchange_type='topic')
    try:
        yield channel
    finally:
        channel.close()
