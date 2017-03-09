import controllers
from controllers.AuthController import AuthController
from configurator import app
import json
from core.utils import HttpCodes
from models.db_worker import connection
from core.exception import RequestException
import datetime

class BaseActioner(object):
    """
    Базовый класс для actioner.
    Также используется для идентификации actioner
    """
    actioner_name = 'default'

    def __init__(self):
        self.curuser = None
        self.register_data = None
        self._control = None
        self._method = None
        self.login = None
        self.password = None
        self.token = None
        self._registered = False

    def is_registered(self):
        return self._registered

    # def register_action(self, control, method, dict_param):
    #     raise NotImplementedError

    @classmethod
    def get_name(cls):
        return cls.actioner_name

    @staticmethod
    def get_element(obj, attr_name, postfix='', errmess=u'не найден элемент'):
        """
        поиск атрибутов в объекте
        :param obj: объект для поиска
        :param attr_name: str название аттрибута
        :param postfix: str добивка названия
        :param errmess: текст ошибки если не найден атрибут
        """
        for var in dir(obj):
            if var.lower() == (attr_name + postfix).lower():
                break
        else:
            var = ''  # если прошли цикл и ничего не нашли, то обнуляем
        attr = getattr(obj, var, None)
        if attr is None or not callable(attr):
            raise RequestException(errmess=errmess, errcode=HttpCodes.bed_request)
        return attr

    # def register_action(self):
    #     pass

    def run_action(self):
        raise NotImplementedError


class ApiActioner(BaseActioner):
    actioner_name = 'api'

    def __init__(self):
        super().__init__()

    def check_auth(self, conn):
        checker = AuthController(conn)
        checker.check_token(self.token)
        self.curuser = checker.get_curuser()
        return self.curuser

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


class AuthActioner(BaseActioner):
    actioner_name = 'auth'

    def __init__(self):
        super().__init__()

    def check_auth(self, conn):
        checker = AuthController(conn)
        checker.check_auth(self.login, self.password)
        self.token = checker.get_token()
        return self.token

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
