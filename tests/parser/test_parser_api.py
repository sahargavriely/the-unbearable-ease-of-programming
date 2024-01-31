from pathlib import Path

import pytest

from brain_computer_interface.message import CONFIG_OPTIONS
from brain_computer_interface.parser import parse
from brain_computer_interface.utils import keys


def test_parse_bad_parser_name():
    bad_name = 'no such parser'
    with pytest.raises(ValueError, match='We want looking everywhere '
                       f'but did not find {bad_name!r} parser'):
        parse(bad_name, {}, Path())


def test_parse(server_data, parsed_data, tmp_path):
    for topic in CONFIG_OPTIONS:
        parsed_topic = parse(topic, server_data[topic], tmp_path)[keys.data]
        expected_parsed = parsed_data[topic][keys.data]
        if keys.data in (keys.color_image, keys.depth_image):
            assert parsed_topic[keys.height] == expected_parsed[keys.height]
            assert parsed_topic[keys.width] == expected_parsed[keys.width]
        else:
            assert parsed_topic == expected_parsed
