# from flask import
from src.models.user import User
from src.models.db_worker import DBException


class UserController(object):

    def __init__(self, cursor):
        self.cursor = cursor
        self.user_login = None  # user_login
        self.curuser = None
        self.message = None

    def authenticate(self, user_login, user_pass):
        try:
            self.curuser = User.get_user_by_login(self.cursor, user_login)
            if self.curuser.password == user_pass:
                return True
        except DBException as e:
            self.message = e.args[0]
        else:
            self.message = 'failed password'
        return
