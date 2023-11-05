import datetime as dt

import pytest

from brain_computer_interface.utils import Thought

from utils import Dictionary

_USER_ID = 1
_TIMESTAMP = dt.datetime(2000, 1, 1, 10, 0)
_THOUGHT = "I'm hungry"
_ENCODE_THOUGHT = b"\x01\x00\x00\x00\x00\x00\x00\x00\x00" \
    b"\xb4m8\x00\x00\x00\x00\n\x00\x00\x00I'm hungry"


@pytest.fixture
def thought():
    return Thought(_USER_ID, _TIMESTAMP, _THOUGHT)


def test_attributes(thought: Thought):
    assert thought.user_id == _USER_ID
    assert thought.timestamp == _TIMESTAMP
    assert thought.thought == _THOUGHT


def test_repr(thought: Thought):
    assert thought.__repr__() == f'Thought(user_id={_USER_ID!r}, '\
        f'timestamp={_TIMESTAMP!r}, thought={_THOUGHT!r})'


def test_str(thought: Thought):
    assert thought.__str__() == \
        f'[{_TIMESTAMP:%Y-%m-%d %H:%M:%S}] user {_USER_ID}: {_THOUGHT}'


def test_file_format(thought: Thought):
    assert thought.file_formatted_timestamp == \
        f'{_TIMESTAMP:%Y-%m-%d_%H-%M-%S}'


def test_eq(thought: Thought):
    t1 = Thought(_USER_ID, _TIMESTAMP, _THOUGHT)
    assert t1 == thought
    t2 = Thought(_USER_ID + 1, _TIMESTAMP, _THOUGHT)
    assert t2 != thought
    t3 = Thought(_USER_ID, _TIMESTAMP + dt.timedelta(minutes=1), _THOUGHT)
    assert t3 != thought
    t4 = Thought(_USER_ID, _TIMESTAMP, _THOUGHT + '!')
    assert t4 != thought
    t5 = 1
    assert t5 != thought
    t6 = Dictionary({
        'user_id': _USER_ID,
        'timestamp': _TIMESTAMP,
        'thought': _THOUGHT,
    })
    assert t6 != thought


def test_serialize(thought: Thought):
    assert thought.serialize() == _ENCODE_THOUGHT


def test_deserialize(thought):
    thought_decrypted = Thought.deserialize(_ENCODE_THOUGHT)
    assert thought_decrypted.user_id == _USER_ID
    assert thought_decrypted.timestamp == _TIMESTAMP
    assert thought_decrypted.thought == _THOUGHT
    assert thought_decrypted == thought


def test_symmetry(thought: Thought):
    assert Thought.deserialize(thought.serialize()) == thought
