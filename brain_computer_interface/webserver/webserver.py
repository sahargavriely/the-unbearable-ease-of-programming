from http import HTTPStatus
from pathlib import Path

import flask

from ..utils import (
    LISTEN_HOST,
    SERVER_PORT,
    SHARED_DIR,
)


_INDEX_HTML = '''<html>
    <head>
        <title>Brain Computer Interface</title>
    </head>
    <body>
        <ul>
            {users}
        </ul>
    </body>
</html>
'''
_USER_LINE_HTML = '''
<li><a href="/users/{user_id}">user {user_id}</a></li>
'''
_USER_HTML = '''
<html>
    <head>
        <title>Brain Computer Interface: User {user_id}</title>
    </head>
    <body>
        <table>
            {thoughts}
        </table>
    </body>
</html>
'''
_THOUGHT_HTML = '''
<tr>
    <td>{time}</td>
    <td>{thought}</td>
</tr>
'''
_USER_NOT_FOUND_HTML = '''
<html>
    <head>
        <title>Brain Computer Interface: User {user_id}</title>
    </head>
    <body>
        <p>We want looking everywhere but did not found user {user_id}</p>
    </body>
</html>
'''


def run_webserver(
    host: str = LISTEN_HOST,
    port: int = SERVER_PORT,
    data_dir: Path = SHARED_DIR,
    debug: bool = False
):
    app = flask.Flask(__name__)
    data_dir = Path(data_dir)

    @app.route('/')
    def index():
        users = set()
        if data_dir.exists():
            users = set([user.name for user in data_dir.iterdir()])
        users_html = list()
        for user_dir in users:
            users_html.append(_USER_LINE_HTML.format(user_id=user_dir))
        index_html = _INDEX_HTML.format(users='\n'.join(users_html))
        return index_html, HTTPStatus.OK

    @app.route('/users/<string:user_id>')
    def user(user_id):
        users = set()
        if data_dir.exists():
            users = set([user.name for user in data_dir.iterdir()])
        if user_id not in users:
            user_not_found_html = _USER_NOT_FOUND_HTML.format(user_id=user_id)
            return user_not_found_html, HTTPStatus.NOT_FOUND
        thoughts_html = list()
        for file in (data_dir / user_id).iterdir():
            date, hour = file.name.split('.')[0].split('_')
            time = ' '.join([date, hour.replace('-', ':')])
            thought = file.read_text()
            thought_html = _THOUGHT_HTML.format(time=time, thought=thought)
            thoughts_html.append(thought_html)
        thoughts = '\n'.join(thoughts_html)
        user_html = _USER_HTML.format(user_id=user_id, thoughts=thoughts)
        return user_html, HTTPStatus.OK

    app.run(host, port, debug)
