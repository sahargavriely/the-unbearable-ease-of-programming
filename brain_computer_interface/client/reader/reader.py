from ...message import Snapshot
from ...utils import get_driver, setup_logging


logger = setup_logging(__name__)


class Reader:
    def __init__(self, path: str):
        logger.info('initiating reader for path %s', path)
        extension = path.split('.')[-1]
        self.driver = get_driver(
            __file__, __package__, 'extension', extension)(path)
        self.file_pointer = 0
        with self as file:
            logger.debug('reading user')
            self.user = self.driver.read_user(file)

    def __iter__(self):
        return self

    def __next__(self) -> Snapshot:
        with self as file:
            if not file.peek(1):
                logger.info('reach end of stream')
                raise StopIteration('No more snapshots to read')
            logger.debug('reading snapshot')
            return self.driver.read_snapshot(file)

    def __enter__(self):
        self.file = self.driver.open()
        logger.debug('seeking to %s', self.file_pointer)
        self.file.seek(self.file_pointer)
        return self.file

    def __exit__(self, exception, error, traceback):
        if self.file:
            self.file_pointer = self.file.tell()
            logger.debug('reach to %s', self.file_pointer)
            self.file.close()
            del self.file
