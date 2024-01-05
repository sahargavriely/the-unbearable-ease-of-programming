import pytest


from brain_computer_interface.distributer import Distributer


def test_distributer_driver_scheme_error():
    bad_scheme = 'sike'
    url = f'{bad_scheme}:///nowhere'
    error_msg = f'Could not locate distributer driver scheme {bad_scheme!r}'
    with pytest.raises(ValueError, match=error_msg):
        Distributer(url)


def test_file_distributer_driver(tmp_path):
    # tmp_path.mkdir(exist_ok=True, parents=True)
    data = 'fe!n'
    url = f'file://{str(tmp_path.absolute())}/data.json'
    file_driver = Distributer(url)
    file_driver.publish_raw_snapshot(data)
    assert data == file_driver.subscribe()
