import json
from pathlib import Path

from ..utils import Snapshot


parsers = list()


def parser(parser_name):
    def decorator(obj):
        parsers.append((parser_name, obj))
        return obj
    return decorator


@parser('translation')
def parse_translation(cur_user_dir: Path, snapshot: Snapshot):
    x, y, z = snapshot.translation
    with (cur_user_dir / 'translation.json').open('w') as file:
        json.dump(dict(x=x, y=y, z=z), file)


@parser('color_image')
def parse_color_image(cur_user_dir: Path, snapshot: Snapshot):
    snapshot.color_image.save(cur_user_dir / 'color_image.jpg')
