from core.tokenWallet import tokenizer
from models import User, Chat, Message
from models.db_worker import DBException
from core.exception import RequestException
from core.utils import HttpCodes
import datetime


class AuthController(object):

    def __init__(self, conn):
        self.conn = conn
        self.token = None
        self.curuser = None

    def _db_user(self, login):
        try:
            user = User.get_user_by_login(self.conn, login)
        except DBException as e:
            raise RequestException(errmess=e.args[0], errcode=HttpCodes.not_found)
        return user

    # TODO: переделать ошибки в классы ошибок
    def check_token(self, token):
        login = tokenizer.get_login(token)
        if login is None:
            raise RequestException(errmess='Нет авторизации', errcode=HttpCodes.unauthorized)
        self.curuser = self._db_user(login)

    def check_auth(self, login, password):
        user = self._db_user(login)
        if not password == user.password:
            raise RequestException(errmess='Неверная пара логина и пароля', errcode=HttpCodes.unauthorized)
        self.curuser = user

    def get_token(self):
        self.token = tokenizer.get_token(self.curuser.login)
        return self.token

    def get_curuser(self):
        return self.curuser
