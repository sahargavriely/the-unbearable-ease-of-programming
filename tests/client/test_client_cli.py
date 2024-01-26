import subprocess

from brain_computer_interface.message import (
    Snapshot,
    User,
)
from tests.client.utils import assert_now


def test_read(default_mind_file, snapshot: Snapshot, user: User):
    cmd = ['python', '-m', 'brain_computer_interface.client', 'read',
           str(default_mind_file)]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    process.wait(1)
    stdout, _ = process.communicate()
    assert repr(user) in stdout.decode()
    assert repr(snapshot) in stdout.decode()


def test_compressed_read(protobuf_mind_file, snapshot: Snapshot, user: User):
    cmd = ['python', '-m', 'brain_computer_interface.client', 'read',
           str(protobuf_mind_file)]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    process.wait(1)
    stdout, _ = process.communicate()
    assert repr(user) in stdout.decode()
    assert repr(snapshot) in stdout.decode()


def test_upload_mind(conf, default_mind_file, protobuf_mind_file, user,
                     snapshot, get_message):
    cmd = ['python', '-m', 'brain_computer_interface.client', 'upload-mind',
           '-h', conf.REQUEST_HOST, '-p', str(conf.SERVER_PORT),
           str(default_mind_file)]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    process.wait(3)
    stdout, _ = process.communicate()
    assert b'snapshot uploaded' in stdout.lower()
    assert user.name.lower().encode() in stdout.lower()
    decoded_user, decoded_snapshots, popped_key = get_message()
    snapshot.set_default(popped_key)
    assert decoded_user == user.serialize()
    assert repr(Snapshot.from_bytes(decoded_snapshots[0])) == repr(snapshot)

    cmd = ['python', '-m', 'brain_computer_interface.client', 'upload-mind',
           '-h', conf.REQUEST_HOST, '-p', str(conf.SERVER_PORT),
           str(protobuf_mind_file)]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    process.wait(3)
    stdout, _ = process.communicate()
    assert b'snapshot uploaded' in stdout.lower()
    assert user.name.lower().encode() in stdout.lower()
    decoded_user, decoded_snapshots, popped_key = get_message()
    snapshot.set_default(popped_key)
    assert decoded_user == user.serialize()
    assert repr(Snapshot.from_bytes(decoded_snapshots[0])) == repr(snapshot)


def test_upload_thought(conf, get_message):
    cmd = ['python', '-m', 'brain_computer_interface.client',
           'upload-thought', '-h', conf.REQUEST_HOST,
           '-p', str(conf.SERVER_PORT), str(conf.USER_20), conf.THOUGHT_20]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    process.wait(3)
    stdout, _ = process.communicate()
    assert b'done' in stdout.lower()
    user_id, timestamp, thought = get_message()
    assert user_id == conf.USER_20
    assert_now(timestamp)
    assert thought == conf.THOUGHT_20


def test_upload_thought_error(conf):
    cmd = ['python', '-m', 'brain_computer_interface.client',
           'upload-thought', '-h', conf.REQUEST_HOST,
           '-p', str(conf.SERVER_PORT), str(conf.USER_20), conf.THOUGHT_20]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    process.wait(1)
    stdout, _ = process.communicate()
    assert b'error' in stdout.lower()
