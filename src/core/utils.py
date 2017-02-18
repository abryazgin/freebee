from controllers import UserController
from configurator import app
from flask import request, redirect, url_for, g, session, escape
from werkzeug.local import LocalProxy
from functools import wraps
import mysql.connector


def get_db():
    db = getattr(g, '_database', None)
    # app.logger.info('get_db')
    if db is None:
        # app.logger.info('get_db_create')
        db_conf = app.config.get_namespace('DB_')
        db = g._database = mysql.connector.connect(**db_conf)
        # db = g._database = conn.cursor(dictionary=True)
    return db


@app.teardown_appcontext
def teardown_db(exception):
    db = getattr(g, '_database', None)
    # app.logger.info('teardown_db')
    if db is not None:
        # app.logger.info('teardown_db_close')
        db.close()

db = LocalProxy(get_db)


def auth(func):
    @wraps(func)
    def wrapper(*arg, **kw):
        username = str(escape(session.get('login')))
        password = str(escape(session.get('password')))
        # username = request.cookies.get('login')
        cur = db.cursor(dictionary=True)
        if username:
            control = UserController(cur)
            if control.authenticate(username, password):
            # if user.password == request.cookies.get('password'):
                resp = func(*arg, **kw)
                return resp
        return redirect(url_for('login'))
    return wrapper


def log_request(func):
    @wraps(func)
    def wrapper(*arg, **kw):
        app.logger.info('call method {} with list={} and dict={}'.format(func.__name__, arg, kw))
        res = func(*arg, **kw)
        return res
    return wrapper


def _attr_parser_helper(obj, mapa):
    """
    проходит вглубь объекта и выводит его атрибуты
    :param obj: объект
    :param mapa: карта параметров вида {'id':None, 'name':None, 'user':{'id':None}}
    :return: словарь параметров
    """
    param = {}
    for attr in mapa:
        if not hasattr(obj, attr):
            continue
        attr_val = getattr(obj, attr)
        param[attr] = _attr_parser_helper(attr_val, mapa[attr]) if mapa[attr] else attr_val
    return param


def attr_parser(data_list, mapa):
    """
    проходит вглубь объектов и выводит их атрибуты
    :param data_list: список объектов
    :param mapa: карта параметров вида {'id':None, 'name':None, 'user':{'id':None}}
    :return: список словарей параметров
    """
    constructed = []
    for obj in data_list:
        param_build = _attr_parser_helper(obj, mapa)
        constructed.append(param_build)
    return constructed