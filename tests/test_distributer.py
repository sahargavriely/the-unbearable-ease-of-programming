import multiprocessing
import queue
import time
import threading

import pytest

from brain_computer_interface.distributer import Distributer
from brain_computer_interface.message.message import CONFIG_OPTIONS
from brain_computer_interface.utils import keys


def test_file_distributer_driver(tmp_path):
    data = 'fe!n'
    url = f'file://{str(tmp_path.absolute())}/'
    file_driver = Distributer(url)
    file_driver.publish(data, 'test-file')
    ret_data = {}

    def callback(_data):
        nonlocal ret_data
        ret_data = _data

    file_driver.subscribe(callback, 'test-file')
    assert data == ret_data


def test_rabbitmq_distributer_driver_bad_values():
    bad_addr = '127.0.0.1:88'
    url = f'rabbitmq://{bad_addr}/'
    error_msg = f'Failed to connect - bad values were given {bad_addr}'
    with pytest.raises(ValueError, match=error_msg):
        Distributer(url).connect()


def test_rabbitmq_distributer_server(rabbitmq, conf, snapshot, user, tmp_path):
    topics = [keys.user, *CONFIG_OPTIONS]
    q = queue.Queue()

    def sub(func, topic):
        with Distributer(conf.RABBITMQ_SCHEME) as distributer:
            getattr(distributer, func)(q.put, topic)

    for topic in topics:
        func = 'subscribe' if topic == keys.user else 'subscribe_raw_topic'
        threading.Thread(target=sub, args=(func, topic,), daemon=True).start()

    time.sleep(7)
    with Distributer(conf.RABBITMQ_SCHEME) as distributer:
        user = user.jsonify()
        data = {keys.user: user}
        distributer.publish_server(data)
        snapshot = snapshot.jsonify(tmp_path)
        data[keys.snapshot] = snapshot
        distributer.publish_server(data)

    for _ in range(len(topics)):
        result = q.get(timeout=5)
        topic = result[keys.metadata][keys.topic]
        topics.remove(topic)
        if topic == keys.user:
            assert result[keys.data] == user
        else:
            result = result[keys.data]
            if keys.data in snapshot[topic]:
                assert result[keys.height] == snapshot[topic][keys.height]
                assert result[keys.width] == snapshot[topic][keys.width]
            else:
                assert result == snapshot[topic]
    assert not topics


def test_rabbitmq_distributer_parsed(rabbitmq, conf):
    with Distributer(conf.RABBITMQ_SCHEME) as distributer:
        parent, child = multiprocessing.Pipe()
        key = 'parsed-key'
        thread = threading.Thread(target=distributer.subscribe_parsed_topic,
                                  args=(child.send, key, 'test-group'),
                                  daemon=True)
        thread.start()
        time.sleep(.1)
        data = '<parsed data here>'
        with Distributer(conf.RABBITMQ_SCHEME) as another:
            another.publish_parsed_topic(data, key)
        if not parent.poll(5):
            raise TimeoutError()
        assert data == parent.recv()
