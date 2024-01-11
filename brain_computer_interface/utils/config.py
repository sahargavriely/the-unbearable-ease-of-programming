from pathlib import Path


LISTEN_HOST = '0.0.0.0'
REQUEST_HOST = '127.0.0.1'
SERVER_PORT = 5000
SHARED_DIR = Path('shared/')
DISTRIBUTE_SCHEME = f'file://{SHARED_DIR.absolute()}/published/'
WEBSERVER_PORT = 8000
