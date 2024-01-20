import datetime as dt
from pathlib import Path
import subprocess
import shutil
import time

import furl
import pytest

from brain_computer_interface.database import Database
from brain_computer_interface.message import (
    DepthImage,
    ColorImage,
    Config,
    CONFIG_OPTIONS,
    Feelings,
    Pose,
    Rotation,
    Snapshot,
    Translation,
    User,
)
from brain_computer_interface.utils import config as config_module, keys
from utils import (
    Dictionary,
    _run_webserver,
    _serve_thread,
)


##########################################################################
# Configuration


@pytest.fixture(scope='session')
def other_conf():
    return Dictionary({
        'RABBITMQ_SCHEME': 'rabbitmq://localhost:4561/',
        'USER_20': 20,
        'THOUGHT_20': 'I am 20 too',
        'TIMESTAMP_20':
            int(dt.datetime(2019, 10, 25, 15, 12, 5, 228000).timestamp()),
        'USER_22': 22,
        'THOUGHT_22': 'I am 22',
        'TIMESTAMP_22':
            int(dt.datetime(2019, 10, 25, 15, 15, 2, 304000).timestamp()),
    })


@pytest.fixture(scope='session')
def patch_conf(tmp_path_factory):
    tmp_path = tmp_path_factory.mktemp('shared')
    return Dictionary({
        'DATABASE': f'file://{Path(tmp_path).absolute()}/database/',
        'DISTRIBUTE_SCHEME': f'file://{Path(tmp_path).absolute()}/published/',
        'LISTEN_HOST': '0.0.0.0',
        'REQUEST_HOST': '127.0.0.1',
        'SERVER_PORT': 5356,
        'SHARED_DIR': Path(tmp_path),
        'WEBSERVER_PORT': 8356,
    })


@pytest.fixture(scope='session')
def conf(patch_conf, other_conf):
    other_conf.update(patch_conf)
    other_conf.WEBSERVER_URL = \
        f'http://{other_conf.REQUEST_HOST}:{other_conf.WEBSERVER_PORT}'
    return other_conf


@pytest.fixture(autouse=True)
def patch(monkeypatch, patch_conf):
    for key, value in patch_conf.items():
        if hasattr(config_module, key):
            monkeypatch.setattr(config_module, key, value)


@pytest.fixture(autouse=True)
def clean_db(conf):
    if conf.SHARED_DIR.exists():
        shutil.rmtree(str(conf.SHARED_DIR))


##########################################################################
# Parser


@pytest.fixture
def parsed_data(user, snapshot, tmp_path):
    datetime = dt.datetime.fromtimestamp(snapshot.datetime / 1000)
    imgs_dir = tmp_path / str(user.id) / f'{datetime:%F_%H-%M-%S-%f}'
    imgs_dir.mkdir(parents=True, exist_ok=True)
    user = user.jsonify()
    snap = snapshot.jsonify(imgs_dir)
    metadata = dict(user_id=user[keys.id], datetime=snap[keys.datetime])
    data = dict()
    for topic in CONFIG_OPTIONS:
        metadata_ = metadata.copy()
        metadata_['topic'] = topic
        data[topic] = dict(metadata=metadata_, data=snap[topic])
    return data


##########################################################################
# Database


@pytest.fixture()
def database(conf):
    yield Database(conf.DATABASE)
    shutil.rmtree(str(furl.furl(conf.DATABASE).path))


##########################################################################
# Distributer


@pytest.fixture(scope='session')
def rabbitmq(conf):
    url = furl.furl(conf.RABBITMQ_SCHEME)
    subprocess.call(['docker', 'run', '--detach', '--publish',
                     f'{url.port}:5672', '--hostname', 'my-test-rabbit',
                     '--name', 'test-rabbit', 'rabbitmq'], timeout=5)
    time.sleep(6)
    yield
    subprocess.call(['docker', 'stop', 'test-rabbit'], timeout=30)
    subprocess.call(['docker', 'remove', 'test-rabbit'], timeout=5)


##########################################################################
# Message


@pytest.fixture(scope='module')
def config():
    return Config(CONFIG_OPTIONS)


@pytest.fixture(scope='module')
def snapshot():
    return Snapshot(
        int(time.time() * 1000),
        Pose(
            Translation(.1, .2, .3),
            Rotation(.1, .2, .3, .4)
        ),
        ColorImage(1, 1, b'\x00\x00\x00'),
        DepthImage(1, 1, [.5]),
        Feelings(.1, .2, .3, .4)
    )


@pytest.fixture(scope='module')
def user():
    return User(
        1,
        'Sahar Gavriely',
        int(dt.datetime.strptime('June 6, 1994', '%B %d, %Y').timestamp()),
        0
    )


##########################################################################
# Server


@pytest.fixture(scope='module')
def webserver(conf):
    with _serve_thread(_run_webserver, conf) as thread:
        yield thread
