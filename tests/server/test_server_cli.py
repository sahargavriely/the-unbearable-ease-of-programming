import datetime as dt
import signal
import subprocess
import time

from utils import (
    _get_path,
    mock_upload_mind,
    mock_upload_thought,
)


def test_run_server(conf, user, snapshot):
    cmd = ['python', '-m', 'brain_computer_interface.server', 'run-server',
           '-h', conf.LISTEN_HOST, '-p', str(conf.SERVER_PORT),
           '-d', str(conf.DATA_DIR)]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
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
    datetime = dt.datetime.fromtimestamp(snapshot.datetime / 1000)
    mind_path = conf.DATA_DIR / f'{user.id}/{datetime:%F_%H-%M-%S-%f}'
    assert mind_path.exists()
    assert mind_path.is_dir()
