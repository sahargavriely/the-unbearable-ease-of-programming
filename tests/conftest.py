import datetime as dt
import gzip
from pathlib import Path
import shutil
from struct import pack
import subprocess
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
from brain_computer_interface.parser.parsers import (
    DepthImageParser,
    ColorImageParser,
)
from brain_computer_interface.client.reader.drivers.protobuf import \
    length_format
from brain_computer_interface.utils import config as config_module, keys

from tests.utils import Dictionary


##########################################################################
# Configuration


@pytest.fixture(scope='session')
def other_conf():
    return Dictionary({
        'POSTGRES_SCHEME':
            'postgresql://postgres:password@127.0.0.1:4321/testmind',
        'RABBITMQ_SCHEME': 'rabbitmq://localhost:4561/',
    })


@pytest.fixture(scope='session')
def patch_conf(tmp_path_factory):
    tmp_path = Path(tmp_path_factory.mktemp('shared')).absolute()
    return Dictionary({
        'DATABASE_SCHEME': f'file://{tmp_path}/database/',
        'DISTRIBUTE_SCHEME': f'file://{tmp_path}/published/',
        'LISTEN_HOST': '0.0.0.0',
        'REST_SERVER_PORT': 8467,
        'REQUEST_HOST': '127.0.0.1',
        'SERVER_PORT': 5356,
        'SHARED_DIR': tmp_path,
    })


@pytest.fixture(scope='session')
def conf(patch_conf, other_conf):
    other_conf.update(patch_conf)
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
def server_data(user: User, snapshot: Snapshot, tmp_path):
    datetime = dt.datetime.fromtimestamp(snapshot.datetime / 1000)
    imgs_dir = tmp_path / str(user.id) / f'{datetime:%F_%H-%M-%S-%f}'
    imgs_dir.mkdir(parents=True, exist_ok=True)
    usr = user.jsonify()
    snap = snapshot.jsonify(imgs_dir)
    metadata = dict(user_id=usr[keys.id], datetime=snap[keys.datetime])
    data = dict()
    for topic in CONFIG_OPTIONS:
        metadata_ = metadata.copy()
        metadata_[keys.topic] = topic
        data[topic] = dict(metadata=metadata_, data=snap[topic])
    return data


@pytest.fixture
def parsed_data(user: User, snapshot: Snapshot, conf):
    datetime = dt.datetime.fromtimestamp(snapshot.datetime / 1000)
    imgs_dir = conf.SHARED_DIR / str(user.id) / f'{datetime:%F_%H-%M-%S-%f}'
    imgs_dir.mkdir(parents=True, exist_ok=True)
    usr = user.jsonify()
    snap = snapshot.jsonify(imgs_dir)
    snap[keys.color_image] = \
        ColorImageParser().parse(snap[keys.color_image], imgs_dir)
    snap[keys.depth_image] = \
        DepthImageParser().parse(snap[keys.depth_image], imgs_dir)
    metadata = dict(user_id=usr[keys.id], datetime=snap[keys.datetime])
    data = dict()
    for topic in CONFIG_OPTIONS:
        metadata_ = metadata.copy()
        metadata_[keys.topic] = topic
        data[topic] = dict(metadata=metadata_, data=snap[topic])
    return data


##########################################################################
# Database


@pytest.fixture()
def database(conf):
    db = Database(conf.DATABASE_SCHEME)
    yield db
    db.drop_db()


@pytest.fixture(scope='session')
def postgres(conf):
    url = furl.furl(conf.POSTGRES_SCHEME)
    name = 'test-postgres'
    subprocess.call(['docker', 'run', '--detach', '--publish',
                     f'{url.port}:5432', '--hostname', 'my-test-postgres',
                     f'--env=POSRGRES_USER={url.username}',
                     f'--env=POSTGRES_PASSWORD={url.password}',
                     '--name', name, 'postgres'], timeout=60)
    time.sleep(4)
    yield
    subprocess.call(['docker', 'stop', name], timeout=30)
    subprocess.call(['docker', 'remove', name], timeout=5)


##########################################################################
# Distributer


@pytest.fixture(scope='session')
def rabbitmq(conf):
    url = furl.furl(conf.RABBITMQ_SCHEME)
    name = 'test-rabbit'
    subprocess.call(['docker', 'run', '--detach', '--publish',
                     f'{url.port}:5672', '--hostname', 'my-test-rabbit',
                     '--name', name, 'rabbitmq'], timeout=60)
    time.sleep(6)
    yield
    subprocess.call(['docker', 'stop', name], timeout=30)
    subprocess.call(['docker', 'remove', name], timeout=5)


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
# Mind file


@pytest.fixture(scope='module')
def mind_dir(tmp_path_factory):
    return tmp_path_factory.mktemp('minds')


@pytest.fixture(scope='module')
def protobuf_mind_file(mind_dir: Path, user: User, snapshot: Snapshot):
    file = mind_dir / 'sample.mind.gz'
    file.touch(0o777)
    with gzip.open(str(file), 'wb') as f:
        f.write(pack(length_format, len(user.serialize())))
        f.write(user.serialize())
        f.write(pack(length_format, len(snapshot.serialize())))
        f.write(snapshot.serialize())
    return file
