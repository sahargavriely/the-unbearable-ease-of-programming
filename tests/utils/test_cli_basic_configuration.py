import shutil
import subprocess

import pytest


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
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, )
    stdout, _ = process.communicate()
    assert b'something went terribly wrong :[' in stdout.lower()


def test_quiet_flag(some_script):
    cmd = ['python', str(some_script), '-q', 'error']
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, )
    stdout, _ = process.communicate()
    assert not stdout.lower()


def test_traceback_flag(some_script):
    cmd = ['python', str(some_script), '-t', 'error']
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, )
    stdout, _ = process.communicate()
    assert b'traceback (most recent call last)' in stdout.lower()
