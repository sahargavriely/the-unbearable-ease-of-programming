import json

from brain_computer_interface.message import Snapshot

from tests.server.utils import mock_upload_mind


def test_run_server(conf, server, server_publish_file, user, snapshot):
    assert not server_publish_file.exists()
    mock_upload_mind(conf, user, snapshot)
    assert server_publish_file.exists()
    assert server_publish_file.is_file()
    with server_publish_file.open('r') as file:
        data = json.load(file)
    user_json = data['user']
    snapshot_json = data['snapshot']
    assert user.jsonify() == user_json
    assert repr(snapshot) == repr(Snapshot.from_json(snapshot_json))
    assert snapshot.color_image.data == Snapshot.from_json(
        snapshot_json).color_image.data
    assert snapshot.depth_image.data == Snapshot.from_json(
        snapshot_json).depth_image.data
