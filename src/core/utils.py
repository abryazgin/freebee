from ..models.user import User
from ..models.db_worker import get_db
from flask import request, redirect, url_for
from functools import wraps


def auth(func):
    @wraps(func)
    def wrapper(*arg, **kw):
        username = request.args.get('login')
        # username = request.cookies.get('login')
        db = get_db()
        cur = db.cursor()
        if username:
            user = User.get_user_by_login(cur, username)
            if user.password == request.args.get('password'):
            # if user.password == request.cookies.get('password'):
                resp = func(*arg, **kw)
                return resp
        return redirect(url_for('login'))
    return wrapper
