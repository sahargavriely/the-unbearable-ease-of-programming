import json
import pathlib

import furl


class FileScheme:
    scheme = 'file'

    def __init__(self, url: furl.furl):
        self.path = pathlib.Path(str(url.path))

    def publish(self, data):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open('w') as f:
            json.dump(data, f)

    def subscribe(self):
        with self.path.open('r') as f:
            return json.load(f)
