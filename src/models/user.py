#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import db_worker
import logging
import chat


class User:
    def __init__(self, id, login, email, role, password):
        self.id = id
        self.login = login
        self.email = email
        self.password = password
        self.role = role

    def __str__(self):
        return 'id = {0},\tlogin = {1},\temail = {2},\tpassword = {3},\trole = {4}'.format(
                self.id, self.login, self.email, self.role, self.password)

    @staticmethod
    def get_all_users(conn):
        users = db_worker.execute(conn, 'CALL GET_ALL_USERS()')
        return [User(*u) for u in users]

    @staticmethod
    def get_user_by_id(conn, id):
        u = db_worker.execute(conn, 'CALL GET_USER_BY_ID(%s)', (id,))
        if len(u) == 0:
            logging.write('Пользователя № %s не существует!' % id)
            return None
        u = u[0]
        # id, login, email, password, role = u
        current_user = User(*u)
        return current_user

    @staticmethod
    def get_user_by_login(conn, log):
        u = db_worker.execute(conn, 'CALL GET_USER_BY_LOGIN(%s)', (log,))
        if len(u) == 0:
            logging.write('Пользователя %s не существует!' % log)
            return None
        u = u[0]
        current_user = User(*u)
        return current_user

    def get_chat_list(self, conn):
        chats = db_worker.execute(conn, 'CALL GET_CHAT_LIST_BY_USER_ID(%s)', (self.id,))
        return [chat.Chat(*ch) for ch in chats]


if __name__ == '__main__':
    db = db_worker.get_db()
    cursor = db.cursor()

    # Поиск всех пользователей
    logging.write('----------------\nВсе пользователи:')
    user_list = User.get_all_users(cursor)
    for u in user_list:
        logging.write(u)
        current_user_chats_list = u.get_chat_list(cursor)
        logging.write('Список чатов %s:' % u.login)
        for ch in current_user_chats_list:
            logging.write(ch)
        logging.write('')

    # Поиск пользователя по логину
    log = 'admin'
    logging.write('----------------\nПользователь %s:' % log)
    user_admin = User.get_user_by_login(cursor, log)
    logging.write(user_admin)

    # Поиск списка чатов пользователя
    admin_chat_list = user_admin.get_chat_list(cursor)
    for chat in admin_chat_list:
        logging.write(chat)

    # Поиск пользователя по id
    id = 2
    logging.write('----------------\nПользователь id = %s' % id)
    user2 = User.get_user_by_id(cursor, id)
    logging.write(user2)

    # sql-инъекция
    log = 'john\'); DROP database freebee;-- '
    logging.write('----------------\nПользователь %s:' % log)
    user_drop_table = User.get_user_by_login(cursor, log)
    logging.write(user_drop_table)

    # Поиск пользователя, отсутствующего в базе
    log = 'dfghjskdlf'
    logging.write('----------------\nПользователь %s:' % log)
    user_nonsense = User.get_user_by_login(cursor, log)
    logging.write(user_nonsense)

    cursor.close()
    db.close()
