
import gzip
from pathlib import Path
import multiprocessing
import pytest
from struct import pack


from brain_computer_interface.client.reader.drivers.default import (
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
from brain_computer_interface.client.reader.drivers.protobuf import \
    length_format
from brain_computer_interface.message import Snapshot, User
from utils import _run_mock_server


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
# Server


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
