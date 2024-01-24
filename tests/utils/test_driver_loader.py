import shutil
import sys

import pytest

from brain_computer_interface.utils import get_driver


predict_key = 'predict_key'
predict = 'predict'


@pytest.fixture(scope='module')
def divers_package(tmp_path_factory):
    tmp_path = tmp_path_factory.mktemp('tmp')
    drivers = tmp_path / 'drivers'
    drivers.mkdir(parents=True, exist_ok=True)
    driver = drivers / 'driver.py'
    (tmp_path / '__init__.py').touch()
    with driver.open('w') as file:
        file.write(f'class Driver: {predict_key}={predict!r}')
    sys.path.append(str(tmp_path.parent))
    yield tmp_path
    shutil.rmtree((tmp_path))


@pytest.fixture(scope='module')
def some_file(divers_package):
    file = (divers_package / f'{divers_package.name}.py')
    file.touch()
    return file


def test_get_driver_error(some_file, divers_package):
    bad_predict = 'sike'
    error_msg = f'Could not locate driver {predict_key} {bad_predict!r}'
    with pytest.raises(ValueError, match=error_msg):
        get_driver(some_file, divers_package.name, predict_key, bad_predict)


def test_get_driver(some_file, divers_package):
    driver = get_driver(some_file, divers_package.name, predict_key, predict)
    assert hasattr(driver, predict_key)
    assert getattr(driver, predict_key) == predict
