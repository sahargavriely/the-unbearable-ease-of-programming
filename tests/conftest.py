import datetime as dt
import gzip
from pathlib import Path
import shutil
from struct import pack
import time

import docker
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


def pytest_collection_modifyitems(session, config, items):
    start = list()
    middle = list()
    end = list()
    for item in items:
        if item.module.__name__ == 'test_end_to_end':
            end.append(item)
        elif 'utils' in str(item.path):
            start.append(item)
        else:
            middle.append(item)
    items[:] = start + middle + end


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
    client = docker.from_env()
    image = client.images.pull('postgres')
    container = client.containers.run(image=image, detach=True, name=name,
                                      ports={5432: url.port}, remove=True,
                                      hostname='my-test-postgres',
                                      environment={
                                          'POSTGRES_USER': url.username,
                                          'POSTGRES_PASSWORD': url.password})
    time.sleep(3)
    yield
    container.stop()


##########################################################################
# Distributer


@pytest.fixture(scope='session')
def rabbitmq(conf):
    url = furl.furl(conf.RABBITMQ_SCHEME)
    name = 'test-rabbit'
    client = docker.from_env()
    image = client.images.pull('rabbitmq')
    container = client.containers.run(image=image, detach=True, name=name,
                                      ports={5672: url.port}, remove=True,
                                      hostname='my-test-rabbit')
    time.sleep(3)
    yield
    container.stop()


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
