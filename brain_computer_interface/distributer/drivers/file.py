import json
import pathlib

import furl


# For testing purposes
class FileScheme:
    scheme = 'file'

    def __init__(self, url: furl.furl):
        self.path = pathlib.Path(str(url.path))

    def publish_raw_snapshot(self, data):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open('w') as f:
            json.dump(data, f)

    def subscribe(self, callback):
        with self.path.open('r') as f:
            callback(json.load(f))
