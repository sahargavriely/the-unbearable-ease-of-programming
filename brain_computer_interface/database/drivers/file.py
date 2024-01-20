import datetime as dt
import json
import pathlib

import furl

from brain_computer_interface.utils import keys


# For testing purposes
class FileScheme:
    scheme = 'file'
    dt_format = '%Y-%m-%d_%H-%M-%S-%f'

    def __init__(self, url: furl.furl):
        self.path = pathlib.Path(str(url.path))
        self.path.mkdir(parents=True, exist_ok=True)

    def save_user(self, user_id, data):
        (self.path / str(user_id)).mkdir(parents=True, exist_ok=True)
        with (self.path / str(user_id) / keys.user).open('w') as f:
            json.dump(data, f)

    def save_snapshot_topic(self, user_id, datetime, topic, data):
        datetime = dt.datetime.fromtimestamp(datetime / 1000)
        snap_dir = self.path / str(user_id) / f'{datetime:%F_%H-%M-%S-%f}'
        snap_dir.mkdir(parents=True, exist_ok=True)
        with (snap_dir / topic).open('w') as f:
            json.dump(data, f)

    def get_users(self):
        return list(int(user.name) for user in self.path.iterdir())

    def get_user(self, user_id):
        user_file = self.path / str(user_id) / keys.user
        if not user_file.exists():
            return dict()
        with user_file.open('r') as f:
            return json.load(f)

    def get_user_snapshots(self, user_id):
        user_dir = self.path / str(user_id)
        if not user_dir.exists():
            return list()
        snapshots = list()
        for item in user_dir.iterdir():
            if item.is_dir():
                datetime = dt.datetime.strptime(item.name, self.dt_format)
                datetime = int(datetime.timestamp() * 1000)
                snapshots.append(datetime)
        return snapshots

    def get_user_snapshot(self, user_id, datetime):
        datetime = dt.datetime.fromtimestamp(datetime / 1000)
        snap_dir = self.path / str(user_id) / f'{datetime:%F_%H-%M-%S-%f}'
        if not snap_dir.exists():
            return dict()
        snapshot = dict()
        for topic in snap_dir.iterdir():
            if topic.is_file():
                with topic.open('r') as f:
                    snapshot[topic.name] = json.load(f)
        return snapshot

    def get_user_snapshot_topic(self, user_id, datetime, topic):
        datetime = dt.datetime.fromtimestamp(datetime / 1000)
        topic_dir = self.path / str(user_id) \
            / f'{datetime:%F_%H-%M-%S-%f}' / topic
        with topic_dir.open('r') as f:
            return json.load(f)
