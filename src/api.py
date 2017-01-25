from flask import Blueprint, g, redirect, url_for, request, session
from src.core.utils import auth, db
# from src.core.utils import get_connector
from .controllers import ChatController, UserController

app_api = Blueprint('api', __name__)


@app_api.route('/chat')
@auth
def all_chat():
    cur = db.cursor(dictionary=True)
    control = ChatController(cur)
    res = control.run()
    return res if res else redirect(url_for('/login'))


@app_api.route('/chat/<string:chat_name>')
@auth
def cur_chat(chat_name):
    control = ChatController()
    res = control.run(chat_name)
    if res is None:
        return redirect(url_for('/chat'))


@app_api.route('/chat/test')
@auth
def test_chat():
    control = ChatController()
    return control.run()


@app_api.route('/login', methods=['GET'])
# @app_api.route('/login')
def login():
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
def index():
    return 'please, get me a lot of money for develop this page'
