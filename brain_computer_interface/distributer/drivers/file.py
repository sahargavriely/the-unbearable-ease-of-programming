import json
import pathlib

import furl


# For testing purposes
class FileScheme:
    scheme = 'file'

    def __init__(self, url: furl.furl):
        self.path = pathlib.Path(str(url.path))
        self.path.mkdir(parents=True, exist_ok=True)

    def publish(self, data, topic):
        with (self.path / topic).open('w') as f:
            json.dump(data, f)

    def subscribe(self, callback, topic, *_, **__):
        with (self.path / topic).open('r') as f:
            callback(json.load(f))
