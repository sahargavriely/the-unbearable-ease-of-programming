import pytest

from brain_computer_interface.utils import TypedProperty


@pytest.fixture
def A():
    class A:
        x = TypedProperty(int)
        y = TypedProperty(str)
    return A


@pytest.fixture
def a(A):
    return A()


def test_get(a):
    assert a.x == 0
    assert a.y == ''


def test_set(a):
    a.x = 1
    assert a.x == 1
    a.y = 'Hello, world!'
    assert a.y == 'Hello, world!'


def test_set_error(a):
    with pytest.raises(ValueError):
        a.x = 'Hello, world!'
    with pytest.raises(ValueError):
        a.y = 1


def test_delete(a):
    a.x = 1
    del a.x
    assert a.x == 0
    del a.x
    assert a.x == 0
    a.y = 'Hello, world!'
    del a.y
    assert a.y == ''
    del a.y
    assert a.y == ''


def test_get_class(A):
    assert isinstance(A.x, TypedProperty)
    assert isinstance(A.y, TypedProperty)
