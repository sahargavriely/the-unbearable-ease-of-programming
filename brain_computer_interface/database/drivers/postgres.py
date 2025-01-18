import furl
import psycopg2
from psycopg2.errors import ForeignKeyViolation
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2.extras import RealDictCursor
from psycopg2.sql import Identifier, SQL

from brain_computer_interface.utils import keys


class PostgreSQL:
    scheme = 'postgresql'

    def __init__(self, url: furl.furl):
        self.url = url
        self.db_name = str(url.path).removeprefix('/')
        db_exists = False
        conn = _create_pg_conn(url)
        with conn.cursor() as curs:
            curs.execute(IS_DB_EXISTS, [self.db_name])
            db_exists = curs.fetchall()[0][0]
        if not db_exists:
            self._create_db(url)
        else:
            self.conn = _create_pg_conn(url, db_name=self.db_name)

    def _create_db(self, url: furl.furl):
        conn = _create_pg_conn(url)
        with conn.cursor() as curs:
            curs.execute(SQL('CREATE DATABASE {}')
                         .format(Identifier(self.db_name)))
        conn.close()
        self.conn = _create_pg_conn(url, db_name=self.db_name)
        with self.conn.cursor() as curs:
            curs.execute(CREATE_USER_TABLE)
            curs.execute(CREATE_TRANSLATION_TABLE)
            curs.execute(CREATE_ROTATION_TABLE)
            curs.execute(CREATE_POSE_TABLE)
            curs.execute(CREATE_COLOR_IMAGE_TABLE)
            curs.execute(CREATE_DEPTH_IMAGE_TABLE)
            curs.execute(CREATE_FEELINGS_TABLE)
            curs.execute(CREATE_SNAPSHOT_TABLE)

    def save_user(self, user_id, data):
        with self.conn.cursor() as curs:
            data[keys.id] = user_id
            # user is a saved word so PG doesn't allow to use it
            return _insert(curs, 'users', **data)

    def save_snapshot_topic(self, user_id, datetime, topic, data):
        snapshot = {keys.datetime: datetime, topic: data}
        try:
            self._inner_save_snapshot_topic(user_id, snapshot)
        except ForeignKeyViolation:
            self.save_user(user_id, dict(name='snapshot with no user'))
            self._inner_save_snapshot_topic(user_id, snapshot)

    def _inner_save_snapshot_topic(self, user_id, snapshot):
        with self.conn.cursor() as curs:
            return _insert(curs, keys.snapshot,
                           prim_key=f'{keys.datetime}, user_id',
                           user_id=user_id, **snapshot)

    def get_users(self):
        with self.conn.cursor() as curs:
            curs.execute('SELECT id FROM users')
            return list(row[0] for row in curs.fetchall())

    def get_user(self, user_id):
        with self.conn.cursor(cursor_factory=RealDictCursor) as curs:
            curs.execute('SELECT * FROM users WHERE id = (%s)', [user_id])
            ret = curs.fetchone() or dict()
            return {key: val for key, val in ret.items()}

    def get_user_snapshots(self, user_id):
        with self.conn.cursor() as curs:
            curs.execute('SELECT datetime FROM snapshot WHERE user_id = (%s)',
                         [user_id])
            return list(row[0] for row in curs.fetchall())

    def get_user_snapshot(self, user_id, datetime):
        with self.conn.cursor() as curs:
            curs.execute(GET_SNAPSHOT, [user_id, datetime])
            ret, = curs.fetchone() or (dict(),)
            _pop_id_key(ret)
            return ret

    def get_user_snapshot_topic(self, user_id, datetime, topic):
        snapshot = self.get_user_snapshot(user_id, datetime)
        return snapshot.get(topic, dict())

    def drop_db(self):
        self.conn.close()
        conn = _create_pg_conn(self.url)
        with conn.cursor() as curs:
            curs.execute(f'DROP DATABASE {self.db_name}')


def _pop_id_key(dictionary: dict):
    dictionary.pop(keys.id, None)
    for val in dictionary.values():
        if isinstance(val, dict):
            _pop_id_key(val)


def _create_pg_conn(url: furl.furl, db_name=''):
    # postgres is the default name because it is always exists in pg servers
    # meaning with can connect to it always.
    # unlike other names which will not exists if not specifically created.
    db_name = db_name or 'postgres'
    conn = psycopg2.connect(database=db_name, host=url.host, user=url.username,
                            password=url.password, port=url.port)
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
    prim_keys_amount = 1 + prim_key.count(',')
    update_keys = ', '.join(table_keys[prim_keys_amount:])
    exclude_update_keys = 'EXCLUDED.' + \
        ', EXCLUDED.'.join(table_keys[prim_keys_amount:])
    curs.execute(
        f'INSERT INTO {table_name} ({insert_keys}) VALUES ({values_format}) '
        f'ON CONFLICT ({prim_key}) '
        f'DO UPDATE SET ({update_keys}) = ROW({exclude_update_keys}) '
        f'RETURNING {prim_key}',
        table_values)
    if prim_keys_amount == 1:
        return curs.fetchone()[0]
    return curs.fetchone()


IS_DB_EXISTS = '''
    select exists(
        SELECT datname
        FROM pg_catalog.pg_database
        WHERE datname = (%s)
    );
'''
CREATE_USER_TABLE = '''
    CREATE TABLE users (
        id INTEGER PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        birthday INTEGER,
        gender INTEGER
    );
'''
CREATE_TRANSLATION_TABLE = '''
    CREATE TABLE translation (
        id SERIAL PRIMARY KEY,
        x FLOAT,
        y FLOAT,
        z FLOAT
    );
'''
CREATE_ROTATION_TABLE = '''
    CREATE TABLE rotation (
        id SERIAL PRIMARY KEY,
        x FLOAT,
        y FLOAT,
        z FLOAT,
        w FLOAT
    );
'''
CREATE_POSE_TABLE = '''
    CREATE TABLE pose (
        id SERIAL PRIMARY KEY,
        translation INTEGER REFERENCES translation(id),
        rotation INTEGER REFERENCES rotation(id)
    );
'''
CREATE_COLOR_IMAGE_TABLE = '''
    CREATE TABLE color_image (
        id SERIAL PRIMARY KEY,
        width INTEGER,
        height INTEGER,
        data VARCHAR(255)
    );
'''
CREATE_DEPTH_IMAGE_TABLE = '''
    CREATE TABLE depth_image (
        id SERIAL PRIMARY KEY,
        width INTEGER,
        height INTEGER,
        data VARCHAR(255)
    );
'''
CREATE_FEELINGS_TABLE = '''
    CREATE TABLE feelings (
        id SERIAL PRIMARY KEY,
        hunger FLOAT,
        thirst FLOAT,
        exhaustion FLOAT,
        happiness FLOAT
    );
'''
CREATE_SNAPSHOT_TABLE = '''
    CREATE TABLE snapshot (
        user_id INTEGER REFERENCES users(id),
        datetime BIGINT,
        pose INTEGER REFERENCES pose(id),
        color_image INTEGER REFERENCES color_image(id),
        depth_image INTEGER REFERENCES depth_image(id),
        feelings INTEGER REFERENCES feelings(id),
        PRIMARY KEY (datetime, user_id)
    );
'''
GET_SNAPSHOT = '''
    SELECT json_build_object(
        'datetime', s.datetime,
        'pose', json_build_object('translation', t.*, 'rotation', r.*),
        'color_image', c.*,
        'depth_image', d.*,
        'feelings', f.*)
    FROM snapshot AS s
        LEFT JOIN pose AS p ON s.pose = p.id
        LEFT JOIN translation AS t ON p.translation = t.id
        LEFT JOIN rotation AS r ON p.rotation = r.id
        LEFT JOIN color_image AS c ON s.color_image = c.id
        LEFT JOIN depth_image AS d ON s.depth_image = d.id
        LEFT JOIN feelings AS f ON s.feelings = f.id
    WHERE s.user_id = (%s) AND s.datetime = (%s);
'''
