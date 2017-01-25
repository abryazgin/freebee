from ..controllers import UserController
from flask import request, redirect, url_for, g, session, escape
from werkzeug.local import LocalProxy
from functools import wraps
import mysql.connector


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = mysql.connector.connect(host='localhost',
                                                     user='freebee',
                                                     passwd='221uml?Po',
                                                     db='freebee',
                                                     charset='utf8')
        # db = g._database = conn.cursor(dictionary=True)
    return db

db = LocalProxy(get_db)


def auth(func):
    @wraps(func)
    def wrapper(*arg, **kw):
        print(session.get('login'), escape(session.get('login')))
        username = escape(session.get('login'))
        password = escape(session.get('password'))
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

