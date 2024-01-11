import pathlib
import signal
import subprocess
import time

from furl import furl
import pytest

from brain_computer_interface.distributer import Distributer
from brain_computer_interface.message import (
    ColorImage,
    CONFIG_OPTIONS,
    DepthImage,
)
from brain_computer_interface.utils import keys
from utils import (
    _get_path,
    mock_upload_mind,
    mock_upload_thought,
)


def test_run_server_by_scheme(conf, user, snapshot):
    cmd = ['python', '-m', 'brain_computer_interface.server', 'run-server',
           '-d', str(conf.DISTRIBUTE_SCHEME), '-h', conf.LISTEN_HOST,
           '-p', str(conf.SERVER_PORT), '-s', str(conf.SHARED_DIR)]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    published_data_file = \
        pathlib.Path(str(furl(conf.DISTRIBUTE_SCHEME).path))
    assert not published_data_file.exists()
    try:
        time.sleep(0.5)
        args = conf, conf.USER_20, conf.TIMESTAMP_20, conf.THOUGHT_20
        mock_upload_thought(*args)
        args = conf, conf.USER_22, conf.TIMESTAMP_22, conf.THOUGHT_22
        mock_upload_thought(*args)
        mock_upload_mind(conf, user, snapshot)
        time.sleep(0.1)
    finally:
        # we are doing the sig thingy instead of terminate to increase coverage
        process.send_signal(signal.SIGINT)
    thought_path_1 = _get_path(conf.SHARED_DIR, conf.USER_20,
                               conf.TIMESTAMP_20)
    thought_path_2 = _get_path(conf.SHARED_DIR, conf.USER_22,
                               conf.TIMESTAMP_22)
    assert thought_path_1.read_text() == conf.THOUGHT_20
    assert thought_path_2.read_text() == conf.THOUGHT_22

    assert published_data_file.exists()
    assert published_data_file.is_dir()
    data = {}

    def callback(_data):
        nonlocal data
        data = _data

    for op in CONFIG_OPTIONS:
        Distributer(conf.DISTRIBUTE_SCHEME).subscribe_raw_topic(callback, op)
        assert user.jsonify()['id'] == data['metadata']['user_id']
        snapshot_json = snapshot.jsonify()
        assert snapshot_json['datetime'] == data['metadata']['datetime']
        if keys.color_image in op:
            assert snapshot_json[op] == ColorImage.from_json(
                data['data']).jsonify()
        elif keys.depth_image in op:
            assert snapshot_json[op] == DepthImage.from_json(
                data['data']).jsonify()
        else:
            if isinstance(snapshot_json[op], dict):
                for key in snapshot_json[op]:
                    assert snapshot_json[op][key] == pytest.approx(
                        data['data'][key])
            else:
                assert snapshot_json[op] == pytest.approx(data['data'])
