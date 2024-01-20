import furl
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2.extras import RealDictCursor
# from psycopg2.error import ForeignKeyViolation

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
            data[keys.id] = user_id
            # user is a saved word so PG doesn't allow to use it
            return _insert(curs, 'users', **data)

    def save_snapshot_topic(self, user_id, datetime, topic, data):
        with self.conn.cursor() as curs:
            snapshot = {keys.datetime: datetime, topic: data}
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
        topic_data = self.get_user_snapshot(user_id, datetime)[topic]
        return topic_data.get(keys.data, topic_data)


def _pop_id_key(dictionary: dict):
    dictionary.pop(keys.id, None)
    for val in dictionary.values():
        if isinstance(val, dict):
            _pop_id_key(val)


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
        user_id INTEGER REFERENCES users(id),
        datetime INTEGER,
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
        'pose', json_build_object('transition', t.*, 'rotation', r.*),
        'color_image', c.*,
        'depth_image', d.*,
        'feelings', f.*)
    FROM snapshot AS s
        LEFT JOIN pose AS p ON s.pose = p.id
        LEFT JOIN transition AS t ON p.transition = t.id
        LEFT JOIN rotation AS r ON p.rotation = r.id
        LEFT JOIN color_image AS c ON s.color_image = c.id
        LEFT JOIN depth_image AS d ON s.depth_image = d.id
        LEFT JOIN feelings AS f ON s.feelings = f.id
    WHERE s.user_id = (%s) AND s.datetime = (%s);
'''
