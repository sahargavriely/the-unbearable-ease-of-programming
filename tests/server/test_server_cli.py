import json
import pathlib
import signal
import subprocess
import time

import furl

from brain_computer_interface.protocol import Snapshot
from utils import (
    _get_path,
    mock_upload_mind,
    mock_upload_thought,
)


def test_run_server_by_scheme(conf, user, snapshot):
    cmd = ['python', '-m', 'brain_computer_interface.server', 'run-server',
           '-ps', str(conf.PUBLISH_SCHEME), '-h', conf.LISTEN_HOST,
           '-p', str(conf.SERVER_PORT), '-d', str(conf.DATA_DIR)]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    published_data_file = \
        pathlib.Path(str(furl.furl(conf.PUBLISH_SCHEME).path))
    assert not published_data_file.exists()
    try:
        time.sleep(0.4)
        args = conf, conf.USER_20, conf.TIMESTAMP_20, conf.THOUGHT_20
        mock_upload_thought(*args)
        args = conf, conf.USER_22, conf.TIMESTAMP_22, conf.THOUGHT_22
        mock_upload_thought(*args)
        mock_upload_mind(conf, user, snapshot)
        time.sleep(0.1)
    finally:
        # we are doing the sig thingy instead of terminate to increase coverage
        process.send_signal(signal.SIGINT)
    thought_path_1 = _get_path(conf.DATA_DIR, conf.USER_20, conf.TIMESTAMP_20)
    thought_path_2 = _get_path(conf.DATA_DIR, conf.USER_22, conf.TIMESTAMP_22)
    assert thought_path_1.read_text() == conf.THOUGHT_20
    assert thought_path_2.read_text() == conf.THOUGHT_22

    assert published_data_file.exists()
    assert published_data_file.is_file()
    with published_data_file.open('r') as file:
        data = json.load(file)
    assert user.jsonify() == data['user']
    snapshot_json = data['snapshot']
    assert repr(snapshot) == repr(Snapshot.from_json(snapshot_json))
    assert snapshot.color_image.data == Snapshot.from_json(
        snapshot_json).color_image.data
    assert snapshot.depth_image.data == Snapshot.from_json(
        snapshot_json).depth_image.data
