import multiprocessing
import time

import pytest

from brain_computer_interface.distributer import Distributer


def test_distributer_driver_scheme_error():
    bad_scheme = 'sike'
    url = f'{bad_scheme}:///nowhere'
    error_msg = f'Could not locate distributer driver scheme {bad_scheme!r}'
    with pytest.raises(ValueError, match=error_msg):
        Distributer(url)


def test_file_distributer_driver(tmp_path):
    data = 'fe!n'
    url = f'file://{str(tmp_path.absolute())}/data.json'
    file_driver = Distributer(url)
    file_driver.publish_raw_snapshot(data)
    ret_data = {}

    def callback(_data):
        nonlocal ret_data
        ret_data = _data

    file_driver.subscribe(callback)
    assert data == ret_data


def test_rabbitmq_distributer_driver_bad_values():
    bad_addr = '127.0.0.1:88'
    url = f'rabbitmq://{bad_addr}/'
    error_msg = f'Failed to connect - bad values were given {bad_addr}'
    with pytest.raises(ValueError, match=error_msg):
        Distributer(url).connect()


def test_rabbitmq_distributer_driver(rabbitmq, conf):
    data = {'gomen': 'amanai'}
    with Distributer(conf.RABBITMQ_SCHEME) as distributer:
        distributer.publish_raw_snapshot(data)
        parent, child = multiprocessing.Pipe()
        process = multiprocessing.Process(target=distributer.subscribe,
                                          args=(child.send,))
        process.start()
        try:
            if not parent.poll(5):
                raise TimeoutError()
            assert data == parent.recv()
        finally:
            process.terminate()
            process.join()
