#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import db_worker
import logging


class Chat:
    def __init__(self, in_id, in_name):
        self.id = in_id
        self.name = in_name

    def __str__(self):
        return 'id = {0}, name = {1}'.format(self.id, self.name)

    @staticmethod
    def get_all_messages(conn, chat_id):
        select_result = db_worker.execute(conn, 'CALL GET_MESSAGES(%s)', (chat_id,))
        if len(select_result) == 0:
            logging.write('Не сообщений в чате CHAT_ID = %s' % chat_id)
            return []
        messages_list = []
        for select in select_result:
            id, time, text, sender, chat_name = select
            messages_list.append([id, time, text, sender, chat_name])
        return messages_list

    @staticmethod
    def get_last_messages(conn, chat_id, mess_count):
        select_result = db_worker.execute(conn, 'CALL GET_LAST_MESSAGES(%s)', (chat_id, mess_count))
        if len(select_result) == 0:
            logging.write('Не сообщений в чате CHAT_ID = %s' % chat_id)
            return []
        messages_list = []
        for select in select_result:
            id, time, text, sender, chat_name = select
            messages_list.append([id, time, text, sender, chat_name])
        return messages_list


if __name__ == '__main__':
    db = db_worker.get_db()
    cursor = db.cursor()

    message_list_1 = Chat.get_all_messages(cursor, 1)
    for mess in message_list_1:
        logging.write(mess)

    message_list_2 = Chat.get_all_messages(cursor, 2)
    for mess in message_list_2:
        logging.write(mess)

    cursor.close()
    db.close()
