import ast
import contextlib
import signal
import subprocess
import time

import pytest

from brain_computer_interface.message import CONFIG_OPTIONS
from brain_computer_interface.client import upload_mind
from brain_computer_interface.utils import keys

from tests.utils import Dictionary


def test_end_to_end_finale_form(postgres, rabbitmq, protobuf_mind_file,
                                conf, user, snapshot, parsed_data):
    processes = list()
    db_scheme = conf.POSTGRES_SCHEME
    distribute_scheme = conf.RABBITMQ_SCHEME
    try:
        # rest
        cmd = ['python', '-m', 'brain_computer_interface.rest',
               'run-rest-server', '-h', conf.LISTEN_HOST,
               '-p', str(conf.REST_SERVER_PORT), '-d', db_scheme]
        processes.append(subprocess.Popen(cmd))
        time.sleep(5)
        # parsers
        for topic in CONFIG_OPTIONS:
            cmd = ['python', '-m', 'brain_computer_interface.parser',
                   'run-parser', topic, '-s', str(conf.SHARED_DIR),
                   '-d', distribute_scheme]
            processes.append(subprocess.Popen(cmd))
        time.sleep(5)
        # server
        cmd = ['python', '-m', 'brain_computer_interface.server', 'run-server',
               '-d', distribute_scheme, '-h', conf.LISTEN_HOST,
               '-p', str(conf.SERVER_PORT), '-s', str(conf.SHARED_DIR)]
        processes.append(subprocess.Popen(cmd))
        time.sleep(5)
        # saver
        cmd = ['python', '-m', 'brain_computer_interface.saver', 'run-saver',
               '-d', db_scheme, '-ds', distribute_scheme]
        processes.append(subprocess.Popen(cmd))

        _test_full_setup(protobuf_mind_file, conf, parsed_data, user, snapshot)
    finally:
        for process in processes:
            with contextlib.suppress(Exception):
                # we are doing the sig thingy instead of terminate() or kill()
                # to increase coverage
                process.send_signal(signal.SIGINT)
                process.wait(1)
        time.sleep(2)


def test_run_pipeline(protobuf_mind_file, user, snapshot, parsed_data, conf):
    try:
        with open('.env', 'r') as file:
            original_content = file.readlines()
            test_content = [line.replace('/shared', str(conf.SHARED_DIR))
                            for line in original_content]
        with open('.env', 'w') as file:
            file.write(''.join(test_content))
        subprocess.call(['./scripts/run_pipeline.sh'], timeout=180)
        d_co = Dictionary({
            'REST_SERVER_PORT': 8000,
            'REQUEST_HOST': '127.0.0.1',
            'SERVER_PORT': 5000,
        })

        _test_full_setup(protobuf_mind_file, d_co, parsed_data, user, snapshot)
    finally:
        with open('.env', 'w') as file:
            file.write(''.join(original_content))
        subprocess.call(['docker', 'compose', 'down'], timeout=120)


###############################################################################
# UTILS


def _test_full_setup(protobuf_mind_file, conf, parsed_data, user, snapshot):
    time.sleep(20)
    # client
    upload_mind(str(protobuf_mind_file), conf.REQUEST_HOST, conf.SERVER_PORT)
    time.sleep(20)
    assert _get_command(conf, 'user', user.id) == user.jsonify()
    dt = snapshot.datetime
    expected_snap = dict(datetime=dt)
    for topic in CONFIG_OPTIONS:
        expected_snap[topic] = parsed_data[topic][keys.data]
    saved_snap = _get_command(conf, 'user-snapshot', user.id, dt)
    for key, value in expected_snap.items():
        if isinstance(value, dict):
            for k, v in value.items():
                assert v == pytest.approx(saved_snap[key][k])
        else:
            assert value == pytest.approx(saved_snap[key])
    _get_command(conf, 'user-snapshot-topic-data', user.id, dt,
                 keys.color_image)
    _get_command(conf, 'user-snapshot-topic-data', user.id, dt,
                 keys.depth_image)


def _get_command(conf, *args):
    cmd = ['python', '-m', 'brain_computer_interface.rest', 'get',
           '-h', conf.REQUEST_HOST, '-p', str(conf.REST_SERVER_PORT),
           *[str(arg) for arg in args]]
    pro = subprocess.run(cmd, capture_output=True, check=True, timeout=5)
    ret = pro.stdout.decode().strip()
    try:
        return ast.literal_eval(ret)
    except (ValueError, SyntaxError):
        return dict()
