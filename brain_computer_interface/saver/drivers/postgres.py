import furl
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2.extras import RealDictCursor

from brain_computer_interface.utils import keys


class PostgreSQL:
    scheme = 'postgresql'
    db_name = 'mind'

    def __init__(self, url: furl.furl):
        try:
            self.conn = _create_pg_conn(url, self.db_name)
        except psycopg2.OperationalError as error:
            if f'database "{self.db_name}" does not exist' in str(error):
                self._create_db(url)
            else:
                raise

    def _create_db(self, url: furl.furl):
        conn = _create_pg_conn(url)
        with conn.cursor() as curs:
            curs.execute(f'CREATE DATABASE {self.db_name}')
        conn.close()
        self.conn = _create_pg_conn(url, self.db_name)
        with self.conn.cursor() as curs:
            curs.execute(CREATE_USER_TABLE)
            curs.execute(CREATE_TRANSITION_TABLE)
            curs.execute(CREATE_ROTATION_TABLE)
            curs.execute(CREATE_POSE_TABLE)
            curs.execute(CREATE_COLOR_IMAGE_TABLE)
            curs.execute(CREATE_DEPTH_IMAGE_TABLE)
            curs.execute(CREATE_FEELINGS_TABLE)
            curs.execute(CREATE_SNAPSHOT_TABLE)

    def save_user(self, user_id, data):
        with self.conn.cursor() as curs:
            # user is a saved word so PG doesn't allow to use it
            return _insert(curs, 'users', **data)

    def save_snapshot_topic(self, topic, user_id, datetime, data):
        with self.conn.cursor() as curs:
            snapshot = {keys.datetime: datetime, topic: data}
            return _insert(curs, keys.snapshot, prim_key=keys.datetime, user_id=user_id, **snapshot)

    def get_users(self):
        with self.conn.cursor() as curs:
            curs.execute('SELECT id FROM users')
            return list(row[0] for row in curs.fetchall())

    def get_user(self, user_id):
        with self.conn.cursor(cursor_factory=RealDictCursor) as curs:
            curs.execute('SELECT * FROM users WHERE id = (%s)', [user_id])
            return {key: val for key, val in curs.fetchall()[0].items()}

    def get_user_snapshots(self, user_id):
        with self.conn.cursor() as curs:
            curs.execute(
                'SELECT datetime FROM snapshot WHERE user_id = (%s)', [user_id])
            return list(row[0] for row in curs.fetchall())

    def get_user_snapshot(self, user_id, datetime):
        with self.conn.cursor(cursor_factory=RealDictCursor) as curs:
            curs.execute(
                'SELECT * FROM snapshot WHERE user_id = (%s) AND datetime = (%s)', [user_id, datetime])
            return curs.fetchall()

    def get_user_snapshot_topic(self, topic, user_id, datetime):
        pass

    def _execute(self):
        pass

def _create_pg_conn(url: furl.furl, db_name='postgres'):
    # postgres is the default name because it is always exists in pg servers
    # meaning with can connect to it always.
    # unlike other names which won't not exists if not specifically created.
    conn = psycopg2.connect(database=db_name, host=url.host,
                            user=url.username, password=url.password,
                            port=url.port)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    return conn


def _insert(curs, table_name, prim_key=keys.id, **kwargs):
    table_keys = list()
    values_format = list()
    table_values = list()
    for key, value in kwargs.items():
        table_keys.append(key)
        values_format.append('%s')
        if isinstance(value, dict):
            value = _insert(curs, key, **value)
        table_values.append(value)
    insert_keys = ', '.join(table_keys)
    values_format = ', '.join(values_format)
    update_keys = ', '.join(table_keys[1:])
    exclude_update_keys = 'EXCLUDED.' + ', EXCLUDED.'.join(table_keys[1:])
    curs.execute(
        f'INSERT INTO {table_name} ({insert_keys}) VALUES ({values_format}) '
        f'ON CONFLICT ({prim_key}) '
        f'DO UPDATE SET ({update_keys}) = ROW({exclude_update_keys}) '
        f'RETURNING {prim_key}',
        table_values)
    return curs.fetchone()[0]



CREATE_USER_TABLE = '''
    CREATE TABLE users (
        id INTEGER PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        birthday INTEGER NOT NULL,
        gender INTEGER NOT NULL
    );
'''
CREATE_TRANSITION_TABLE = '''
    CREATE TABLE transition (
        id SERIAL PRIMARY KEY,
        x FLOAT NOT NULL,
        y FLOAT NOT NULL,
        z FLOAT NOT NULL
    );
'''
CREATE_ROTATION_TABLE = '''
    CREATE TABLE rotation (
        id SERIAL PRIMARY KEY,
        x FLOAT NOT NULL,
        y FLOAT NOT NULL,
        z FLOAT NOT NULL,
        w FLOAT NOT NULL
    );
'''
CREATE_POSE_TABLE = '''
    CREATE TABLE pose (
        id SERIAL PRIMARY KEY,
        transition INTEGER REFERENCES transition(id),
        rotation INTEGER REFERENCES rotation(id)
    );
'''
CREATE_COLOR_IMAGE_TABLE = '''
    CREATE TABLE color_image (
        id SERIAL PRIMARY KEY,
        width INTEGER NOT NULL,
        height INTEGER NOT NULL,
        data VARCHAR(255) NOT NULL
    );
'''
CREATE_DEPTH_IMAGE_TABLE = '''
    CREATE TABLE depth_image (
        id SERIAL PRIMARY KEY,
        width INTEGER NOT NULL,
        height INTEGER NOT NULL,
        data VARCHAR(255) NOT NULL
    );
'''
CREATE_FEELINGS_TABLE = '''
    CREATE TABLE feelings (
        id SERIAL PRIMARY KEY,
        hunger FLOAT NOT NULL,
        thirst FLOAT NOT NULL,
        exhaustion FLOAT NOT NULL,
        happiness FLOAT NOT NULL
    );
'''
CREATE_SNAPSHOT_TABLE = '''
    CREATE TABLE snapshot (
        datetime INTEGER PRIMARY KEY,
        user_id INTEGER REFERENCES users(id),
        pose INTEGER REFERENCES pose(id),
        color_image INTEGER REFERENCES color_image(id),
        depth_image INTEGER REFERENCES depth_image(id),
        feelings INTEGER REFERENCES feelings(id)
    );
'''
