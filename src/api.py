from flask import Blueprint, g, redirect, url_for, request, session
from core.utils import auth, db, log_request
# from core.utils import get_connector
from controllers import ChatController, UserController

app_api = Blueprint('api', __name__)


@app_api.route('/chat/')
@log_request
@auth
def all_chat():
    cur = db.cursor(dictionary=True)
    control = ChatController(cur)
    res = control.run()
    return res if res else redirect(url_for('api.login'))


@app_api.route('/chat/<string:chat_name>')
@log_request
@auth
def cur_chat(chat_name):
    cur = db.cursor(dictionary=True)
    control = ChatController(cur)
    res = control.run(chat_name)
    if res is None:
        return redirect(url_for('api.all_chat'))


@app_api.route('/chat/test')
@log_request
@auth
def test_chat():
    cur = db.cursor(dictionary=True)
    control = ChatController(cur)
    return control.run()


@app_api.route('/login', methods=['GET'])
# @app_api.route('/login')
@log_request
def login():
    ar = request.args
    print(dir(ar), [i for i in ar.lists()], ar.to_dict())
    user_login = request.args.get('login')
    user_pass = request.args.get('password')
    if user_login:
        cur = db.cursor(dictionary=True)
        control = UserController(cur)
        if control.authenticate(user_login, user_pass):
            session['login'] = user_login
            session['password'] = user_pass
            return 'user {} log in'.format(user_login)
        else:
            return control.message
    return 'please, get me a lot of money for develop this page'


@app_api.route('/', methods=['GET'])
@log_request
def index():
    return 'please, get me a lot of money for develop this page'
