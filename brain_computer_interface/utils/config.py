from pathlib import Path


DATA_DIR = Path('data/')
LISTEN_HOST = '0.0.0.0'
REQUEST_HOST = '127.0.0.1'
PUBLISH_SCHEME = f'file://{DATA_DIR.absolute()}'
SERVER_PORT = 5000
WEBSERVER_PORT = 8000
