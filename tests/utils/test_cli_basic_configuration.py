import shutil
import subprocess

import pytest

from brain_computer_interface.utils import log


@pytest.fixture(scope='module')
def some_script(tmp_path_factory):
    tmp_path = tmp_path_factory.mktemp('tmp')
    file = (tmp_path / f'{tmp_path}.py')
    with file.open('w') as f:
        f.write('from brain_computer_interface.utils import module_main_exe; '
                'module_main_exe("test")')
    yield file
    shutil.rmtree((tmp_path))


def test_error(some_script):
    cmd = ['python', str(some_script), 'error']
    stdout = subprocess.run(cmd, capture_output=True, timeout=5).stdout
    assert b'something went terribly wrong :[' in stdout.lower()


def test_quiet_flag(some_script):
    cmd = ['python', str(some_script), '-q', 'error']
    stdout = subprocess.run(cmd, capture_output=True, timeout=5).stdout
    assert not stdout.lower()


def test_traceback_flag(some_script):
    cmd = ['python', str(some_script), '-t', 'error']
    stdout = subprocess.run(cmd, capture_output=True, timeout=5).stdout
    assert b'traceback (most recent call last)' in stdout.lower()


def test_log_nonetype(capsys):
    pre_value = log.traceback
    try:
        log.traceback = True
        msg = 'some message with no errors - no reason for trace'
        log(msg)
        capture = capsys.readouterr()
        assert msg in capture.out
        assert msg not in capture.err
        assert 'NoneType: None' not in capture.out
        assert 'NoneType: None' not in capture.err
    finally:
        log.traceback = pre_value
