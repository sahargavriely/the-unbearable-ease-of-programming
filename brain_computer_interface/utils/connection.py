import socket
import struct

from .logging_setter import setup_logging

logger = setup_logging(__name__)


class Connection:
    length_format = '<I'
    length_size = struct.calcsize(length_format)

    def __init__(self, socket: socket.socket, timeout: float = 0):
        socket.settimeout(timeout)
        self._socket = socket

    def __repr__(self):
        cls_name = self.__class__.__name__
        from_host, from_port = self._socket.getsockname()
        from_address = f'{from_host}:{from_port}'
        to_host, to_port = self._socket.getpeername()
        to_address = f'{to_host}:{to_port}'
        return f'<{cls_name} from {from_address} to {to_address}>'

    def __enter__(self):
        return self

    def __exit__(self, exception, error, traceback):
        self.close()

    @classmethod
    def connect(cls, host: str, port: int, timeout: float = 0):
        socket_ = socket.socket()
        logger.info('connecting to (%s, %s)', host, port)
        socket_.connect((host, port))
        return Connection(socket_, timeout)

    # exposing this for the use of `select` package over this cls
    def fileno(self):
        return self._socket.fileno()

    def send(self, data: bytes):
        logger.debug('sending data %s', data)
        self._socket.sendall(data)

    def send_length_follow_by_value(self, data: bytes):
        logger.debug('sending length data of %s', len(data))
        self.send(struct.pack(self.length_format, len(data)))
        self.send(data)

    def receive(self, size: int):
        chunks = []
        while size > 0:
            chunk = self._socket.recv(size)
            if not chunk:
                logger.error('incomplete data')
                raise RuntimeError('Incomplete data')
            chunks.append(chunk)
            logger.debug('received %s bytes out of %s bytes', len(chunk), size)
            size -= len(chunk)
        return b''.join(chunks)

    def receive_length_follow_by_value(self):
        value_length, = struct.unpack(
            self.length_format, self.receive(self.length_size))
        logger.debug('received length data of %s', value_length)
        return self.receive(value_length)

    def close(self):
        self._socket.close()
