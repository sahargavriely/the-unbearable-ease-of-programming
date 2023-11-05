import socket

from .connection import Connection


class Listener:
    def __init__(self, port: int, host: str = '0.0.0.0', backlog=1000,
                 reuseaddr=True):
        self.backlog = backlog
        self.host = host
        self.port = port
        self.reuseaddr = reuseaddr
        socket_ = socket.socket()
        if self.reuseaddr:
            socket_.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        socket_.settimeout(3)
        self.socket_ = socket_

    def __repr__(self):
        backlog = self.backlog
        host = self.host
        port = self.port
        reuseaddr = self.reuseaddr
        return f'Listener({port=!r}, {host=!r}, {backlog=!r}, {reuseaddr=!r})'

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exception, error, traceback):
        self.stop()

    def start(self):
        self.socket_.bind((self.host, self.port))
        self.socket_.listen(self.backlog)

    def stop(self):
        self.socket_.close()

    def accept(self):
        socket_, _ = self.socket_.accept()
        return Connection(socket_)
