import controllers
from configurator import app
import json


class BaseActionerException(Exception):
    pass


class BaseActioner(object):
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

    def register_action(self, control, method, dict_param):
        control_class = getattr(controllers, control, None)
        self._control = control_class()
        if self._control is None:
            return False
        self._method = getattr(self._control, method, None)
        if self._method is None:
            return False
        self._control.prepare(dict_param)
        self.register_data = {'control': control, 'method': method, 'dict_param': dict_param}
        self._registered = True
        return True

    def log_request(self):
        # params = []
        # for k, v in self._method_kwarg.items():
        #     line = '\n    ' + k + '=' + v
        #     params.append(line)
        # case_params = reduce(lambda accum, param: accum + param, params, '')
        app.logger.info('module : {}, action : {}, params : {}'.format(
            self.register_data['control'],
            self.register_data['method'],
            json.dumps(self.register_data['dict_param'], sort_keys=True, indent=8, separators=(',', ': '))
        ))

    def run_control(self):
        if not self.is_registered():
            raise BaseActionerException
        self.log_request()
        res = self._method(**self.register_data['dict_param'])
        return res