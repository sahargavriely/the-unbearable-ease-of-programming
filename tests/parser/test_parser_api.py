import datetime as dt
from pathlib import Path

# from PIL import Image
import pytest

from brain_computer_interface.message import CONFIG_OPTIONS
from brain_computer_interface.parser import parse
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


def test_parse_bad_parser_name():
    bad_name = 'no such parser'
    with pytest.raises(ValueError, match='We want looking everywhere '
                       f'but did not find {bad_name!r} parser'):
        parse(bad_name, {}, Path())


def test_parse(published_data, user, snapshot, tmp_path):
    datetime = dt.datetime.fromtimestamp(snapshot.datetime / 1000)
    imgs_dir = tmp_path / str(user.id) / f'{datetime:%F_%H-%M-%S-%f}'
    imgs_dir.mkdir(parents=True, exist_ok=True)
    snapshot = snapshot.jsonify(imgs_dir)
    for topic in CONFIG_OPTIONS:
        if 'data' in snapshot[topic]:
            continue
        assert parse(topic, published_data[topic]) == snapshot[topic]


# def test_parser(conf, parser: Parser, snapshot: Snapshot):
#     user_dir = conf.SHARED_DIR / 'some_user'
#     parser.parse(user_dir, snapshot)

#     assert (user_dir / 'function.txt').read_text() == _DATA
#     assert (user_dir / 'class.txt').read_text() == _DATA

#     tran = dict()
#     with (user_dir / 'translation.json').open() as file:
#         tran = json.load(file)
#     assert tran['x'] == snapshot.pose.translation.x, tran
#     assert tran['y'] == snapshot.pose.translation.y
#     assert tran['z'] == snapshot.pose.translation.z

#     color_image = Image.open(user_dir / 'color_image.jpg')
#     assert color_image.width == snapshot.color_image.width
#     assert color_image.height == snapshot.color_image.height
#     assert color_image.tobytes() == snapshot.color_image.data
