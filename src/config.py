import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = {
    'host': 'localhost',
    'user':     'freebee',
    'passwd':   '221uml?Po',
    'db':       'freebee',
    'charset':  'utf8'
}
SECRET_KEY = '3656i6645fhn56687nch65fdswfbvd'

# logging

LOG_DIR = '/home/daniil/howork/freebee_log'
LOG_FILE = 'foo.log'
LOG_FORMAT = '%(name)s-%(levelno)s %(asctime)-15s : %(message)s'
LOG_HANDLER = {
    'filename': os.path.join(LOG_DIR, LOG_FILE),
    'maxBytes': 100000,
    'backupCount': 6
}
