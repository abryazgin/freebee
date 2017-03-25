import controllers
from actioners import BaseActioner
# from controllers.AuthController import AuthController
from configurator import app
import json
from core.utils import HttpCodes
from models.db_worker import connection
from core.exception import RequestException
# import datetime


class ApiActioner(BaseActioner):
    actioner_name = 'api'

    # TODO: переделать обратно в регистер и ран
    def register_action(self, control, method, dict_param, headers):
        """
        метод регистрации действия. Находит контроллер, метод, подготавливает контроллер к работе
        """
        self.token = headers.get('X_auth_token')
        with connection() as conn:
            curuser = self.check_auth(conn)

        control_class = self.get_element(controllers,
                                         control,
                                         postfix='controller',
                                         errmess=u'не найден контроллер {}'.format(control))
        self._control = control_class(curuser)
        self._method = self.get_element(self._control, method, errmess=u'не найден метод {}'.format(method))
        self._control.prepare(dict_param)
        self.register_data = {'control': control, 'method': method, 'dict_param': dict_param, 'headers': headers}
        self._registered = True

    def log_request(self):
        app.logger.info('module : {}, action : {}, params : {}'.format(
            self.register_data['control'],
            self.register_data['method'],
            json.dumps(self.register_data['dict_param'], sort_keys=True, indent=8, separators=(',', ': '))
        ))

    def run_action(self):
        """
        запуск метода
        :return: возвращает результат метода в запрошенном виде
        """
        # self.login = header.get('X_auth_login')
        # self.password = header.get('X_auth_password')
        if not self.is_registered():
            raise RequestException(errmess=u'действие не зарегистрированно', errcode=HttpCodes.serv_err)
        with connection() as conn:
            kwargs = self.register_data['dict_param']
            res = self._method(conn, **kwargs)
            self.log_request()
        return res
