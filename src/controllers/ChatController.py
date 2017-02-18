import inspect
from flask import request, redirect, url_for, session, escape
from models import User, Chat, Message
from controllers import BaseController
from core.exception import RequestException
from core.utils import attr_parser
import datetime


class ChatController(BaseController):

    def __init__(self):
        # карты данных
        self.chat_mapa = {'id': None, 'name': None}
        self.datetime_mapa = {'year': None, 'month': None, 'day': None, 'hour': None, 'minute': None, 'second': None}
        self.message_mapa = {'id': None,
                             'sender': {'id': None},
                             'time': self.datetime_mapa,
                             'text': None,
                             'chat': {'id': None}}
        super().__init__()

    def create_chat(self, chat_name, user_id, **kwargs):
        """
        метод создания чата пользователем. чат при создании привязывается к пользователю
        :return:
        """
        conn = kwargs['_conn']
        chat = Chat(name=chat_name)
        user = User.get_user_by_id(conn, user_id)
        chat.create(conn)
        chat.add_user(conn, user)
        return self.response_wrap(chat.id)

    def user_chat(self, user_id, **kwargs):
        """
        список чатов пользователя
        """
        conn = kwargs['_conn']
        user = User.get_user_by_id(conn, user_id)
        chats = user.get_chat_list(conn)
        resp = attr_parser(chats, self.chat_mapa)
        return self.response_wrap(resp)

    def leave_chat(self, chat_id, user_id, **kwargs): # будет переделано на disable
        """
        отмена подписки пользователя (user_id) на чат (chat_id)
        :exception RequestException если чата у пользователя нет
        """
        conn = kwargs['_conn']
        user = User.get_user_by_id(conn, user_id)
        chats = {str(chat.id): chat for chat in user.get_chat_list(conn)}
        if chat_id not in chats:
            raise RequestException('Пользователь (id={}) не подписан на чат (id={})'.format(user_id, chat_id))
        chat = chats[chat_id]
        chat.remove_user(conn, user)
        return self.response_wrap(True)

    def message_send(self, body, chat_id, user_id, **kwargs):
        """
        отправка сообщения в чат (chat_id) от пользователя (user_id)
        :param body: текст сообщения
        :exception RequestException если чата у пользователя нет
        """
        conn = kwargs['_conn']
        now = datetime.datetime.now()
        user = User.get_user_by_id(conn, user_id)
        chats = {str(chat.id): chat for chat in user.get_chat_list(conn)}
        if chat_id not in chats:
            raise RequestException('Пользователь (id={}) не подписан на чат (id={})'.format(user_id, chat_id))
        chat = chats[chat_id]
        mess = Message(now, body, user, chat)
        mess.create(conn)
        return self.response_wrap(True)

    def message_lst(self, chat_id, user_id, **kwargs):
        """
        метод возвращает список сообщений из чата (chat_id)
        :exception RequestException если чата у пользователя нет
        :param user_id: id пользователя у которого находим чат (chat_id), должно совпадать с пользователем приложения.
            будет перенесено в атрибуты класса
        """
        conn = kwargs['_conn']
        user = User.get_user_by_id(conn, user_id)
        chats = {str(chat.id): chat for chat in user.get_chat_list(conn)}
        if chat_id not in chats:
            raise RequestException('Пользователь (id={}) не подписан на чат (id={})'.format(user_id, chat_id))
        chat = chats[chat_id]
        mess_mass = chat.get_all_messages(conn)
        mapa = self.message_mapa
        resp = attr_parser(mess_mass, mapa)
        return self.response_wrap(resp)


