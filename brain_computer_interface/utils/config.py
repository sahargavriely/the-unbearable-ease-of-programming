from pathlib import Path


DATABASE_SCHEME = 'postgresql://postgres:password@127.0.0.1:5432/mind'
DISTRIBUTE_SCHEME = 'rabbitmq://localhost:5672/'
LISTEN_HOST = '0.0.0.0'
REST_SERVER_PORT = 8000
REQUEST_HOST = '127.0.0.1'
SERVER_PORT = 5000
SHARED_DIR = Path('shared/')
WEBSERVER_PORT = 8000
