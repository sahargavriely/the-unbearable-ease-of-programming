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
        parsed_data = parse(topic, published_data[topic], tmp_path)['data']
        if 'data' in snapshot[topic]:
            assert parsed_data['height'] == snapshot[topic]['height']
            assert parsed_data['width'] == snapshot[topic]['width']
        else:
            assert parsed_data == snapshot[topic]
