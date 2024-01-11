import json
import multiprocessing
import signal
import subprocess
import time

from brain_computer_interface.message import CONFIG_OPTIONS
from brain_computer_interface.distributer import Distributer


def test_parse(published_data, snapshot, tmp_path):
    snapshot = snapshot.jsonify(tmp_path)
    for topic in CONFIG_OPTIONS:
        topic_file = tmp_path / topic
        with topic_file.open('w') as file:
            json.dump(published_data[topic], file)
        cmd = ['python', '-m', 'brain_computer_interface.parser', 'parse',
               topic, str(topic_file), '-s', str(tmp_path)]
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        process.wait(2)
        stdout, _ = process.communicate()
        result = eval(stdout.decode().strip())
        if 'data' in snapshot[topic]:
            assert result['height'] == snapshot[topic]['height']
            assert result['width'] == snapshot[topic]['width']
        else:
            assert result == snapshot[topic]


def test_run_parser(rabbitmq, user, snapshot, tmp_path, conf):
    snapshot = snapshot.jsonify(tmp_path)
    data = {'snapshot': snapshot, 'user': user.jsonify()}
    comm_topic = dict()

    for topic in CONFIG_OPTIONS:
        cmd = ['python', '-m', 'brain_computer_interface.parser', 'run-parser',
               topic, '-s', str(tmp_path), '-d', conf.RABBITMQ_SCHEME]
        sub_process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        parent, child = multiprocessing.Pipe()

        def parsed_topic_sub():
            with Distributer(conf.RABBITMQ_SCHEME) as distributer:
                distributer.subscribe_parsed_topic(child.send, topic, '')

        process = multiprocessing.Process(target=parsed_topic_sub, daemon=True)
        comm_topic[topic] = parent, process, sub_process
        process.start()

    time.sleep(7)
    with Distributer(conf.RABBITMQ_SCHEME) as distributer:
        distributer.publish_raw_snapshot(data)
    for topic in CONFIG_OPTIONS:
        parent, process, sub_process = comm_topic[topic]
        if not parent.poll(5):
            raise TimeoutError()
        result = parent.recv()
        if 'data' in snapshot[topic]:
            assert result['height'] == snapshot[topic]['height']
            assert result['width'] == snapshot[topic]['width']
        else:
            assert result == snapshot[topic]
        process.terminate()
        process.join(1)
        # we are doing the sig thingy instead of terminate() or kill()
        # to increase coverage
        sub_process.send_signal(signal.SIGINT)
        sub_process.wait(1)
