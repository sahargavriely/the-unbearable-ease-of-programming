import shutil

import furl
import pytest

from brain_computer_interface.saver import Saver


@pytest.fixture()
def saver(conf):
    yield Saver(conf.DATABASE)
    shutil.rmtree(str(furl.furl(conf.DATABASE).path))
