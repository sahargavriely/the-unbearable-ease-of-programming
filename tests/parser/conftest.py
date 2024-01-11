import datetime as dt

import pytest

from brain_computer_interface.message import CONFIG_OPTIONS
from brain_computer_interface.utils import keys


@pytest.fixture
def published_data(user, snapshot, tmp_path):
    datetime = dt.datetime.fromtimestamp(snapshot.datetime / 1000)
    imgs_dir = tmp_path / str(user.id) / f'{datetime:%F_%H-%M-%S-%f}'
    imgs_dir.mkdir(parents=True, exist_ok=True)
    user = user.jsonify()
    snap = snapshot.jsonify(imgs_dir)
    metadata = dict(user_id=user[keys.id], datetime=snap[keys.datetime])
    data = dict()
    for topic in CONFIG_OPTIONS:
        data[topic] = dict(metadata=metadata, data=snap[topic])
    return data
