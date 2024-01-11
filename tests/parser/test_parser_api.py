from pathlib import Path

import pytest

from brain_computer_interface.message import CONFIG_OPTIONS
from brain_computer_interface.parser import parse


def test_parse_bad_parser_name():
    bad_name = 'no such parser'
    with pytest.raises(ValueError, match='We want looking everywhere '
                       f'but did not find {bad_name!r} parser'):
        parse(bad_name, {}, Path())


def test_parse(published_data, snapshot, tmp_path):
    snapshot = snapshot.jsonify(tmp_path)
    for topic in CONFIG_OPTIONS:
        if 'data' in snapshot[topic]:
            assert parse(topic, published_data[topic], tmp_path)['height'] \
                == snapshot[topic]['height']
            assert parse(topic, published_data[topic], tmp_path)['width'] \
                == snapshot[topic]['width']
        else:
            assert parse(topic, published_data[topic], tmp_path) \
                == snapshot[topic]
