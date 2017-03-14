#!/usr/bin/python3
# -*- coding:utf-8 -*-

from configurator import app
from request_parser import app_api
from flask_socketio import SocketIO
from sockets import ChatNamespace
# from api import app_api

app.register_blueprint(app_api)
sio = SocketIO(app)

sio.on_namespace(ChatNamespace('/sockchat'))

if __name__ == '__main__':
    # app.run(debug=True)
    sio.run(app, debug=True)

    # from flask_socketio import SocketIOTestClient as tc
    #
    # namespace = '/sockchat'
    #
    # test = tc(app, sio, namespace)
    # test.connect()
    # test.emit('auth', {'token': 'fargjfhnkjb54thjw5i4t4rfjn'}, namespace=namespace)
