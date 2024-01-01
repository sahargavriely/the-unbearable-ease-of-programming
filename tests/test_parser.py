import json
from pathlib import Path

from PIL import Image
import pytest

from brain_computer_interface.message import Snapshot
from brain_computer_interface.parser import Parser


_DATA = 'some data'


@pytest.fixture(scope='module')
def parser():
    parser = Parser()

    @parser('function')
    def test_parse(cur_user_dir: Path):
        (cur_user_dir / 'function.txt').write_text(_DATA)

    @parser('class')
    class TestParser:
        def parse(self, cur_user_dir: Path):
            (cur_user_dir / 'class.txt').write_text(_DATA)

    return parser


def test_parser(conf, parser: Parser, snapshot: Snapshot):
    user_dir = conf.DATA_DIR / 'some_user'
    parser.parse(user_dir, snapshot)

    assert (user_dir / 'function.txt').read_text() == _DATA
    assert (user_dir / 'class.txt').read_text() == _DATA

    tran = dict()
    with (user_dir / 'translation.json').open() as file:
        tran = json.load(file)
    assert tran['x'] == snapshot.pose.translation.x, tran
    assert tran['y'] == snapshot.pose.translation.y
    assert tran['z'] == snapshot.pose.translation.z

    color_image = Image.open(user_dir / 'color_image.jpg')
    assert color_image.width == snapshot.color_image.width
    assert color_image.height == snapshot.color_image.height
    assert color_image.tobytes() == snapshot.color_image.data
