import json
from pathlib import Path

from PIL import Image

from ..protocol import Snapshot


def parse_translation(cur_user_dir: Path, snapshot: Snapshot):
    with (cur_user_dir / 'translation.json').open('w') as file:
        json.dump(dict(
            x = snapshot.pose.translation.x,
            y = snapshot.pose.translation.y,
            z = snapshot.pose.translation.z
        ), file)


parse_translation.field = 'translation'


class ColorImageParser:

    field = 'color_image'

    def parse(self, cur_user_dir: Path, snapshot: Snapshot):
        size = snapshot.color_image.width, snapshot.color_image.height
        image = Image.frombytes('RGB', size, snapshot.color_image.data)
        image.save(cur_user_dir / 'color_image.jpg')
