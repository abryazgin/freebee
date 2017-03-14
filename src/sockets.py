import functools
import datetime
from flask import g, request
from flask_socketio import Namespace, disconnect, join_room, leave_room, send, emit
from controllers.AuthController import AuthController
from models.db_worker import connection


def check_auth(func):
    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        if getattr(g, 'curuser', None):
            res = func(*args, **kwargs)
            return res
        else:
            disconnect()
    return wrapped


class ChatNamespace(Namespace):
    def on_connect(self):
        # pass
        print('foo')
        print(request.namespace)

    def on_disconnect(self):
        pass

    def on_auth(self, data):
        token = data['token']
        print(token)
        try:
            with connection() as conn:
                checker = AuthController(conn)
                checker.check_token(token)
                curuser = checker.get_curuser()
                g.curuser = curuser
                chats = curuser.get_chat_list(conn)
                for ch in chats:
                    room = 'chat{}'.format(ch.id)
                    join_room(room)
                emit('serv_resp', {'chats': str([ch.id for ch in chats])}, namespace='/sockchat')
                return 'hello'
        except Exception as e:
            print('boo')
            print(e)
            disconnect()

    @check_auth
    def on_message(self, data):
        mess = data['mass']
        room = data['room']
        chat = room[4:]
        now = datetime.datetime.now()
        emit(
            'serv_resp',
            {'data': {
                'mess': mess,
                'chat': chat,
                'now': str(now)
                }},
            room=room
        )

    @check_auth
    def on_join(self, data):
        room = data['room']
        join_room(room)

    @check_auth
    def on_leave(self, data):
        room = data['room']
        leave_room(room)

