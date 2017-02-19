from models import User, Chat, Message
from models.db_worker import DBException
from core.exception import RequestException
from core.utils import HttpCodes
import datetime


class AuthController(object):

    def __init__(self, conn, login, password):
        self.conn = conn
        self.login = login
        self.password = password
        self.curuser = None

    def check(self):
        try:
            user = User.get_user_by_login(self.conn, self.login)
        except DBException as e:
            raise RequestException(errmess=e.args[0], errcode=HttpCodes.not_found)
        if not self.password == user.password:
            raise RequestException(errmess='Неверная пара логина и пароля', errcode=HttpCodes.unauthorized)
        self.curuser = user

    def get_curuser(self):
        return self.curuser
