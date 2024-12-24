import json
import multiprocessing
import multiprocessing.connection
import signal
import subprocess
import time

from brain_computer_interface.message import CONFIG_OPTIONS
from brain_computer_interface.distributer import Distributer
from brain_computer_interface.utils import keys


def test_parse(parsed_data, server_data, conf):
    for topic in CONFIG_OPTIONS:
        topic_file = conf.SHARED_DIR / topic
        with topic_file.open('w') as file:
            json.dump(server_data[topic], file)
        cmd = ['python', '-m', 'brain_computer_interface.parser', 'parse',
               topic, str(topic_file), '-s', str(conf.SHARED_DIR)]
        stdout = subprocess.run(cmd, capture_output=True, timeout=5).stdout
        result = eval(stdout.decode().strip())[keys.data]
        expected_parsed = parsed_data[topic][keys.data]
        if keys.data in (keys.color_image, keys.depth_image):
            assert result[keys.height] == expected_parsed[keys.height]
            assert result[keys.width] == expected_parsed[keys.width]
        else:
            assert result == expected_parsed


def test_run_parser(rabbitmq, user, snapshot, parsed_data, conf):
    snapshot = snapshot.jsonify(conf.SHARED_DIR)
    data = {keys.snapshot: snapshot, keys.user: user.jsonify()}
    comm_topic = dict()

    for topic in CONFIG_OPTIONS:
        cmd = ['python', '-m', 'brain_computer_interface.parser', 'run-parser',
               topic, '-s', str(conf.SHARED_DIR), '-d', conf.RABBITMQ_SCHEME]
        sub_process = subprocess.Popen(cmd)
        parent, child = multiprocessing.Pipe()
        args = [conf, child, topic]
        process = multiprocessing.Process(target=_parsed_topic_sub, args=args,
                                          daemon=True)
        comm_topic[topic] = parent, process, sub_process
        process.start()

    time.sleep(7)
    with Distributer(conf.RABBITMQ_SCHEME) as distributer:
        distributer.publish_raw_snapshot(data)
    for topic in CONFIG_OPTIONS:
        parent, process, sub_process = comm_topic[topic]
        if not parent.poll(5):
            raise TimeoutError()
        result = parent.recv()[keys.data]
        expected_parsed = parsed_data[topic][keys.data]
        if keys.data in snapshot[topic]:
            assert result[keys.height] == expected_parsed[keys.height]
            assert result[keys.width] == expected_parsed[keys.width]
        else:
            assert result == expected_parsed
        process.terminate()
        process.join(1)
        # we are doing the sig thingy instead of terminate() or kill()
        # to increase coverage
        sub_process.send_signal(signal.SIGINT)
        sub_process.wait(1)


def _parsed_topic_sub(conf, child: multiprocessing.connection.Connection,
                      topic):
    with Distributer(conf.RABBITMQ_SCHEME) as distributer:
        distributer.subscribe_parsed_topic(child.send, topic, '')
