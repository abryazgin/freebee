import controllers
from configurator import app
import json
from models.db_worker import connection
from core.exception import RequestException


class BaseActioner(object):
    """
    Базовый класс для actioner.
    Также используется для идентификации actioner
    """
    actioner_name = 'default'

    def register_action(self, control, method, dict_param):
        raise NotImplementedError

    @classmethod
    def get_name(cls):
        return cls.actioner_name

    def run_control(self):
        raise NotImplementedError


class ApiActioner(BaseActioner):
    actioner_name = 'api'

    def __init__(self):
        self.register_data = None
        self._control = None
        self._method = None
        self._registered = False

    def is_registered(self):
        return self._registered

    def get_element(self, obj, attr_name, postfix='', errmess=u'не найден элемент'):
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
            raise RequestException(errmess)
        return attr

    def check_auth(self):
        pass

    def register_action(self, control, method, dict_param):
        """
        метод регистрации действия. Находит контроллер, метод, подготавливает контроллер к работе
        """
        control_class = self.get_element(controllers,
                                         control,
                                         postfix='controller',
                                         errmess=u'не найден контроллер {}'.format(control))
        self._control = control_class()
        self._method = self.get_element(self._control, method, errmess=u'не найден метод {}'.format(method))
        self._control.prepare(dict_param)
        self.register_data = {'control': control, 'method': method, 'dict_param': dict_param}
        self._registered = True

    def log_request(self):
        app.logger.info('module : {}, action : {}, params : {}'.format(
            self.register_data['control'],
            self.register_data['method'],
            json.dumps(self.register_data['dict_param'], sort_keys=True, indent=8, separators=(',', ': '))
        ))

    def run_control(self):
        """
        запуск метода
        :return: возвращает результат метода в запрошенном виде
        """
        if not self.is_registered():
            raise RequestException(u'действие не зарегистрированно')
        self.log_request()
        with connection() as conn:
            kwargs = self.register_data['dict_param']
            kwargs['_conn'] = conn
            res = self._method(**kwargs)
        return res