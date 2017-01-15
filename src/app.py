#!/usr/bin/python3
# -*- coding:utf-8 -*-

from flask import Flask
from .api import chat

app = Flask(__name__)
# app.config.from_object('config')
# app.run(debug=True)

app.register_blueprint(chat)

@app.route('/login')
def login():
    return 'please, get me a lot of money for develop this page'