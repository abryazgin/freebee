import json


class BaseController(object):
    """
    Базовый класс для контроллеров Api
    """
    def __init__(self):
        self._handler = None

    def prepare(self, dict_param):
        """
        метод для подготовки контроллера в зависимости от параметров.
        :param dict_param: например dict_param['export']='xml'
        """
        self._dump_param = {}

        def handler(data):
            return json.dumps(data, **self._dump_param)

        self._handler = handler

    def response_wrap(self, data):
        """
        метод приведения данных к определенному виду описанному в self._handler
        :param data:
        """
        if callable(self._handler):
            handler = self._handler
            resp = handler(data)
            return resp
        return data

