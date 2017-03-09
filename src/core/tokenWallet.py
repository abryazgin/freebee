#!/usr/bin/python3
# -*- coding:utf-8 -*-

from flask import Flask, request
from collections import namedtuple
import datetime
import hashlib

app = Flask(__name__)


class TokenWallet(object):
    def __init__(self):
        self.tokens = {}  # {token: TokenSpec(login, cr_time)}
        self.users = {}  # {login: token}
        self._TokenSpec = namedtuple('TokenSpec', ['login', 'cr_time'])

    def to_spec(self, login, time):
        return self._TokenSpec(login, time)

    @staticmethod
    def check_token_time(token_spec):
        check_time = 60 * 60 * 24  # day
        now = datetime.datetime.now()
        delta = now - token_spec.cr_time
        if check_time > delta.total_seconds() > 0:
            return True
        else:
            return False

    @staticmethod
    def check_conflict(token, token_spec):
        if token is not None and token_spec is not None or token is None and token_spec is None:  # либо все, либо ничего
            return
        else:
            raise Exception(u'conflict in TokenWallet')

    def generate_token(self, login):
        now = datetime.datetime.now()
        damp_token = login + '_' + str(now)
        token = hashlib.sha224(bytes(damp_token, 'utf8')).hexdigest()
        token_spec = self._TokenSpec(login, now)
        return token, token_spec

    def set_token(self, token, token_spec):
        old_token = self.get_token_by_login(token_spec.login)
        if old_token:
            self.del_token(old_token)
        self.tokens[token] = token_spec
        self.users[token_spec.login] = token
        return True

    def get_token_spec(self, token):
        token_spec = self.tokens.get(token)
        return token_spec

    def get_token_by_login(self, login):
        token = self.users.get(login)
        return token

    def del_token(self, token):
        token_spec = self.get_token_spec(token)
        if token_spec is None:
            return
        login = token_spec.login
        login_token = self.get_token_by_login(login)
        self.check_conflict(login_token, token_spec)
        del self.tokens[token]
        del self.users[login]

    def get_token(self, login):
        token = self.users.get(login)
        if token:
            token_spec = self.get_token_spec(token)
            if self.check_token_time(token_spec):
                return token
        token, token_spec = self.generate_token(login)
        self.set_token(token, token_spec)
        return token

    def get_login(self, token):
        token_spec = self.get_token_spec(token)
        if token_spec and self.check_token_time(token_spec):
            return token_spec.login
        return

    def get_all_token(self):
        return str(list(self.tokens.keys()))

tokenizer = TokenWallet()



if __name__ == '__main__':
    @app.route('/token/<string:login>/')
    def get_token(login):
        print(request.headers.get('atshygfonnection'))
        return tokenizer.get_token(login)


    @app.route('/method/<string:token>/')
    def get_login(token):
        return tokenizer.get_login(token)


    @app.route('/all/')
    def get_all_token():
        return tokenizer.get_all_token()


    app.run(debug=True)
