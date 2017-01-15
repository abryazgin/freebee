#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import db_worker
import logging
import message
import user


class Chat:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __str__(self):
        return 'id = {0}, name = {1}'.format(self.id, self.name)

    @staticmethod
    def get_all_chats(conn):
        chats = db_worker.execute(conn, 'CALL GET_CHATS()')
        return [Chat(*ch) for ch in chats]

    def get_all_messages(self, conn):
        messages = db_worker.execute(conn, 'CALL GET_MESSAGES(%s)', (self.id,))
        message_list = []
        for mess in messages:
            id, time, text, user_id = mess
            sender = user.User.get_user_by_id(conn, user_id)
            message_list.append(message.Message(id, time, text, sender))
        return message_list
        # return [message.Message(*m) for m in messages]

    def get_last_messages(self, conn, mess_count):
        messages = db_worker.execute(conn, 'CALL GET_LAST_MESSAGES(%s, %s)', (self.id, mess_count))
        message_list = []
        for mess in messages:
            id, time, text, user_id = mess
            sender = user.User.get_user_by_id(conn, user_id)
            message_list.append(message.Message(id, time, text, sender))
        return message_list
        # return [message.Message(*m) for m in messages]


if __name__ == '__main__':
    db = db_worker.get_db()
    cursor = db.cursor()

    # Поиск всех чатов, всех сообщений в каждом чате и последнего сообщения в каждом чате
    chat_list = Chat.get_all_chats(cursor)
    for ch in chat_list:
        logging.write(ch)
        logging.write('Список сообщений:')
        mess_list = ch.get_all_messages(cursor)
        for mess in mess_list:
            logging.write(mess)
        logging.write('Последнее сообщение:')
        last_mess = ch.get_last_messages(cursor, 1)
        for mess in last_mess:
            logging.write(mess)
        logging.write('')

    cursor.close()
    db.close()
