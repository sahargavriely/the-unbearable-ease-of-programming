import contextlib
import ctypes
import threading
import time

from brain_computer_interface import run_webserver


class Dictionary(dict):

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(key)

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError:
            raise AttributeError(key)


def _run_webserver(conf):
    run_webserver(conf.LISTEN_HOST, conf.WEBSERVER_PORT, conf.SHARED_DIR)


@contextlib.contextmanager
def serve_thread(serve, *args):
    thread = threading.Thread(target=serve, args=args)
    thread.start()
    time.sleep(1)
    yield thread
    _kill_serve_thread(thread)
    thread.join()


def _kill_serve_thread(thread: threading.Thread):
    if not thread.is_alive() or thread.ident is None:
        return
    c_thread_id = ctypes.c_long(thread.ident)
    c_key_board_interrupt = ctypes.py_object(KeyboardInterrupt)
    send_exception = ctypes.pythonapi.PyThreadState_SetAsyncExc
    res = send_exception(c_thread_id, c_key_board_interrupt)
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect
        send_exception(c_thread_id, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


def receive_all(connection, size):
    chunks = []
    while size > 0:
        chunk = connection.recv(size)
        if not chunk:
            raise RuntimeError('incomplete data')
        chunks.append(chunk)
        size -= len(chunk)
    return b''.join(chunks)
