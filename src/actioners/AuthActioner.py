# import controllers
# from controllers.AuthController import AuthController
from actioners import BaseActioner
from configurator import app
# import json
from core.utils import HttpCodes
from models.db_worker import connection
from core.exception import RequestException
import datetime


class AuthActioner(BaseActioner):
    actioner_name = 'auth'

    # TODO: переделать обратно в регистер и ран
    def register_action(self, headers):
        self.login = headers.get('X_auth_login')
        self.password = headers.get('X_auth_password')
        self._registered = True

    def log_request(self):
        app.logger.info('user : {}, password : {}, time : {}'.format(
            self.login,
            self.password,
            datetime.datetime.now()
        ))

    def run_action(self):
        """
        запуск метода
        :return: возвращает результат метода в запрошенном виде
        """
        if not self.is_registered():
            raise RequestException(errmess=u'действие не зарегистрированно', errcode=HttpCodes.serv_err)
        with connection() as conn:
            res = self.check_auth(conn)
            self.log_request()
        return res
