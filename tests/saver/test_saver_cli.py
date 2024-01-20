import json
import signal
import subprocess
import time
from brain_computer_interface.distributer import Distributer

from brain_computer_interface.message import CONFIG_OPTIONS
from brain_computer_interface.utils import keys


def test_user(database, conf, user, tmp_path):
    user_file = tmp_path / 'user'
    with user_file.open('w') as file:
        json.dump(user.jsonify(), file)
    user_id = user.id
    cmd = ['python', '-m', 'brain_computer_interface.saver', 'save',
           'user', str(user_id), str(user_file), '-d', conf.DATABASE]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    process.wait(2)
    assert database.get_user(user_id) == user.jsonify()


def test_snapshot(database, conf, user, parsed_data, snapshot, tmp_path):
    user_id = user.id
    datetime = int(snapshot.datetime)
    for topic in CONFIG_OPTIONS:
        topic_file = tmp_path / topic
        with topic_file.open('w') as file:
            json.dump(parsed_data[topic][keys.data], file)
        cmd = ['python', '-m', 'brain_computer_interface.saver', 'save',
               'snapshot', topic, str(user_id), str(datetime), str(topic_file),
               '-d', conf.DATABASE]
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        process.wait(2)
        assert database.get_user_snapshot(user_id, datetime)[topic] \
            == parsed_data[topic][keys.data]


def test_run_saver(rabbitmq, database, user, snapshot, parsed_data, conf):
    user_id = user.id
    datetime = snapshot.datetime
    user = user.jsonify()
    path = parsed_data[keys.color_image][keys.data][keys.data]
    snapshot = snapshot.jsonify(path.removesuffix(keys.color_image))
    cmd = ['python', '-m', 'brain_computer_interface.saver', 'run-saver',
           '-d', conf.DATABASE, '-ds', conf.RABBITMQ_SCHEME]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    time.sleep(7)
    with Distributer(conf.RABBITMQ_SCHEME) as distributer:
        distributer.publish_user(user)
    for topic in CONFIG_OPTIONS:
        with Distributer(conf.RABBITMQ_SCHEME) as distributer:
            distributer.publish(parsed_data[topic], f'parsed.{topic}')
    time.sleep(1)
    # we are doing the sig thingy instead of terminate() or kill()
    # to increase coverage
    process.send_signal(signal.SIGINT)
    process.wait(1)
    assert database.get_user(user_id) == user
    saved_snap = database.get_user_snapshot(user_id, datetime)
    for topic in CONFIG_OPTIONS:
        assert saved_snap[topic] == parsed_data[topic][keys.data]
