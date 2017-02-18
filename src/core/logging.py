import os
import gzip
import logging
from logging.handlers import RotatingFileHandler


class GzRotatingFileHandler(RotatingFileHandler):
    """
    класс ротационного обработчика логов, с архивированием
    """
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.rotator = self._rotator
        self.namer = self._namer

    @staticmethod
    def _rotator(source, dest):
        with open(source, 'rb') as f:
            file_body = f.read()
            with gzip.open(dest, 'wb') as gz_file:
                gz_file.write(file_body)
        os.remove(source)

    @staticmethod
    def _namer(file_name):
        return file_name + '.gz'

# можно использовать для тестов
# from config import LOG_HANDLER
# logger = logging.getLogger()
# handler = GzRotatingFileHandler(**LOG_HANDLER)
# logger.addHandler(handler)
