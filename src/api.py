from flask import Blueprint
from .controllers.ChatController import ChatController

chat = Blueprint('chat', __name__, url_prefix='/chat')

@chat.route('/')
def all_chat():
    control = ChatController()
    return control.run()

@chat.route('/<string:chat_name>')
def cur_chat(chat_name):
    control = ChatController()
    return control.run(chat_name)

