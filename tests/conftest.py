import datetime as dt
import gzip
import json
from pathlib import Path
import multiprocessing
import subprocess
import shutil
from struct import pack
import time

import furl

import pytest

from brain_computer_interface.client.reader.drivers.default_driver import (
    id_format,
    name_len_format,
    birthday_format,
    datetime_format,
    translation_format,
    rotation_format,
    height_format,
    width_format,
    pixel_format,
    feelings_format,
)
from brain_computer_interface.client.reader.drivers.protobuf_driver import \
    length_format
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
from brain_computer_interface.utils import config as config_module
from utils import (
    Dictionary,
    _run_server,
    _run_webserver,
    _run_mock_server,
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
        'LISTEN_HOST': '0.0.0.0',
        'PUBLISH_SCHEME': f'file://{Path(tmp_path).absolute()}/publish/',
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
# Distributer


@pytest.fixture(scope='session')
def rabbitmq(conf):
    url = furl.furl(conf.RABBITMQ_SCHEME)
    subprocess.call(['docker', 'run', '--detach', '--publish',
                     f'{url.port}:5672', '--hostname', 'my-test-rabbit',
                     '--name', 'test-rabbit', 'rabbitmq'], timeout=5)
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
# Reader


@pytest.fixture(scope='module')
def mind_dir(tmp_path_factory):
    return tmp_path_factory.mktemp('minds')


@pytest.fixture(scope='module')
def default_mind_file(mind_dir: Path, user: User, snapshot: Snapshot):
    file = mind_dir / 'sample.mind'
    file.touch(0o777)
    user_bytes = list()
    user_bytes.append(pack(id_format, user.id))
    name = user.name.encode()
    user_bytes.append(pack(name_len_format, len(name)))
    user_bytes.append(name)
    user_bytes.append(pack(birthday_format, user.birthday))
    gender = 'm' if user.gender == 0 else 'f' if user.gender == 1 else 'o'
    user_bytes.append(gender.encode())
    snapshot_bytes = list()
    snapshot_bytes.append(pack(datetime_format, snapshot.datetime))
    tran = snapshot.pose.translation
    translation = tran.x, tran.y, tran.z
    snapshot_bytes.append(pack(translation_format, *translation))
    rot = snapshot.pose.rotation
    rotation = rot.x, rot.y, rot.z, rot.w
    snapshot_bytes.append(pack(rotation_format, *rotation))
    snapshot_bytes.append(pack(height_format, snapshot.color_image.height))
    snapshot_bytes.append(pack(width_format, snapshot.color_image.width))
    snapshot_bytes.append(snapshot.color_image.data)
    snapshot_bytes.append(pack(height_format, snapshot.depth_image.height))
    snapshot_bytes.append(pack(width_format, snapshot.depth_image.width))
    depth_data = list()
    for pixel in snapshot.depth_image.data:
        depth_data.append(pack(pixel_format, pixel))
    snapshot_bytes.append(b''.join(depth_data))
    feels = snapshot.feelings
    feelings = feels.hunger, feels.thirst, feels.exhaustion, feels.happiness
    snapshot_bytes.append(pack(feelings_format, *feelings))
    with file.open('wb') as f:
        f.write(b''.join(user_bytes))
        f.write(b''.join(snapshot_bytes))
    return file


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


##########################################################################
# Servers


@pytest.fixture(scope='module')
def server_publish_file(tmp_path_factory):
    return tmp_path_factory.mktemp('publish') / 'data.json'


@pytest.fixture(autouse=True)
def clean_server_publish_file(server_publish_file):
    if server_publish_file.exists():
        server_publish_file.unlink()


@pytest.fixture(scope='module')
def server(conf, server_publish_file: Path):

    def write_data(data):
        with server_publish_file.open('w') as file:
            json.dump(data, file)

    with _serve_thread(_run_server, write_data, conf) as thread:
        yield thread


@pytest.fixture(scope='module')
def webserver(conf):
    with _serve_thread(_run_webserver, conf) as thread:
        yield thread


@pytest.fixture
def mock_server(conf):
    parent, child = multiprocessing.Pipe()
    process = multiprocessing.Process(target=_run_mock_server,
                                      args=(conf, child))
    process.start()
    parent.recv()
    yield parent
    process.terminate()
    process.join()


@pytest.fixture
def get_message(mock_server):

    def get_message():
        if not mock_server.poll(1):
            raise TimeoutError()
        return mock_server.recv()

    yield get_message
