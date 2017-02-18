import os

PROJECT_NAME = 'FREEBEE'


def _get_env(name, val):
    return os.environ.get(PROJECT_NAME + '_' + name) or val

BASEDIR = os.path.abspath(os.path.dirname(__file__))

DATABASE = {
    'host': _get_env('DB_HOST', 'localhost'),
    'user': _get_env('DB_USER', 'freebee'),
    'passwd': _get_env('DB_PASSWD', '221uml?Po'),
    'db': _get_env('DB_DB', 'freebee'),
    'charset': _get_env('DB_CHARSET', 'utf8')
}
DB_HOST = _get_env('DB_HOST', 'localhost')
DB_USER = _get_env('DB_USER', 'freebee')
DB_PASSWD = _get_env('DB_PASSWD', '221uml?Po')
DB_DB = _get_env('DB_DB', 'freebee')
DB_CHARSET = _get_env('DB_CHARSET', 'utf8')

SECRET_KEY = _get_env('SECRET_KEY', '3656i6$^@@@@^6687nch65fdswfbvd')

# logging

LOG_DIR = _get_env('LOG_DIR', BASEDIR)
LOG_FILE = _get_env('LOG_FILE', 'foo.log')
LOG_FORMAT = _get_env('LOG_FORMAT', '%(name)s-%(levelno)s %(asctime)-15s : %(message)s')

LOG_HANDLER = {
    'filename': _get_env('LOG_HANDLER_FILENAME', os.path.join(LOG_DIR, LOG_FILE)),
    'maxBytes': _get_env('LOG_HANDLER_MAXBYTES', 100000),
    'backupCount': _get_env('LOG_HANDLER_BACKUPCOUNT', 6)
}
