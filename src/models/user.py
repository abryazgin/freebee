#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import db_worker
import logging


class User:
    def __init__(self, in_id, in_login, in_email, in_password, in_role):
        self.id = in_id
        self.login = in_login
        self.email = in_email
        self.password = in_password
        self.role = in_role
        pass

    def __str__(self):
        return 'id = {0},\tlogin = {1},\temail = {2},\tpassword = {3},\trole = {4}'.format(
                self.id, self.login, self.email, self.role, self.password)

    @staticmethod
    def get_all_users(conn):
        select_result = db_worker.execute(conn, 'CALL GET_ALL_USERS()')
        if len(select_result) == 0:
            logging.write('Таблица пользователей пуста!')
            return []
        users_list = []
        for select in select_result:
            id, login, email, role, password = select
            current_user = User(id, login, email, password, role)
            users_list .append(current_user)
        return users_list

    @staticmethod
    def get_user_by_login(conn, log):
        u = db_worker.execute(conn, 'CALL GET_USER_BY_LOGIN(%s)', (log,))
        if len(u) == 0:
            logging.write('Пользователя %s не существует!' % log)
            return None
        u = u[0]
        id, login, email, password, role = u
        current_user = User(id, login, email, password, role)
        return current_user

    @staticmethod
    def get_chat_list(conn, log):
        select_result = db_worker.execute(conn, 'CALL GET_CHAT_LIST_BY_LOGIN(%s)', (log,))
        if len(select_result) == 0:
            logging.write('У пользователя %s нет чатов.' % log)
            return None
        chat_list = []
        for select in select_result:
            id, name = select
            chat_list.append([id, name])
        return chat_list


if __name__ == '__main__':
    db = db_worker.get_db()
    cursor = db.cursor()

    logging.write('Все пользователи:')
    user_list = User.get_all_users(cursor)
    for u in user_list:
        logging.write(u)
        current_user_chats_list = User.get_chat_list(cursor, u.login)
        logging.write('Список чатов %s:' % u.login)
        for chat in current_user_chats_list:
            logging.write(chat)
        logging.write('')

    log = 'admin'
    logging.write('\nПользователь %s:' % log)
    user_admin = User.get_user_by_login(cursor, log)
    logging.write(user_admin)

    admin_chat_list = User.get_chat_list(cursor, log)
    for chat in admin_chat_list:
        logging.write(chat)

    log = 'john\'); DROP database freebee;-- '
    logging.write('\nПользователь %s:' % log)
    user_drop_table = User.get_user_by_login(cursor, log)
    logging.write(user_drop_table)

    log = 'dfghjskdlf'
    logging.write('\nПользователь %s:' % log)
    user_nonsense = User.get_user_by_login(cursor, log)
    logging.write(user_nonsense)

    cursor.close()
    db.close()
