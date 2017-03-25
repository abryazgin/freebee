# import controllers
from controllers.AuthController import AuthController
# from configurator import app
# import json
from core.utils import HttpCodes
# from models.db_worker import connection
from core.exception import RequestException
# import datetime


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

    def check_auth(self, conn):
        checker = AuthController(conn)
        checker.check_token(self.token)
        self.curuser = checker.get_curuser()
        return self.curuser

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

