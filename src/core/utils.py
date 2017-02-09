from controllers import UserController
from configurator import app
from flask import request, redirect, url_for, g, session, escape
from werkzeug.local import LocalProxy
from functools import wraps
import mysql.connector


def get_db():
    db = getattr(g, '_database', None)
    app.logger.info('get_db')
    if db is None:
        app.logger.info('get_db_create')
        db = g._database = mysql.connector.connect(**app.config['DATABASE'])
        # db = g._database = conn.cursor(dictionary=True)
    return db


@app.teardown_appcontext
def teardown_db(exception):
    db = getattr(g, '_database', None)
    app.logger.info('teardown_db')
    if db is not None:
        app.logger.info('teardown_db_close')
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
