from os import pread

from models import db_worker
from models import message


class User:
    ADMIN = 'admin'
    STAFFER = 'staffer'
    CLIENT = 'client'

    def __init__(self, login, email, role, password, id=None):
        self.id = id
        self.login = login
        self.email = email
        self.password = password
        self.role = role

    def __str__(self):
        return 'id = {0},\tlogin = {1},\temail = {2},\tpassword = {3},\trole = {4}'.format(
                self.id, self.login, self.email, self.password, self.role)

    @staticmethod
    def get_all_users(conn):
        """
        :return: list, содержащий всех пользователей, полученных из бд.
        """
        users = db_worker.select_list(conn, 'CALL GET_ALL_USERS()')
        return [User(id=u['USER_ID'],
                     login=u['LOGIN'],
                     email=u['EMAIL'],
                     password=u['PASSWORD'],
                     role=u['ROLE'])
                for u in users]

    @staticmethod
    def get_user_by_id(conn, id):
        """
        :exception: db_worker.DBException, если пользователь с указанным id несуществует
        """
        u = db_worker.select_obj(conn, 'CALL GET_USER_BY_ID(%s)', (id,))
        if not u:
            raise db_worker.DBException('Пользователь с id = {0} не существует.'.format(id))
            # выбрасываем исключение здесь, а не в db_worker, чтобы показать более информативное сообщение
            # (db_worker не знает, какой был запрос)
        return User(id=u['USER_ID'],
                    login=u['LOGIN'],
                    email=u['EMAIL'],
                    password=u['PASSWORD'],
                    role=u['ROLE'])

    @staticmethod
    def get_user_by_login(conn, log):
        """
        :exception: db_worker.DBException, если пользователь с указанным логином несуществует
        """
        u = db_worker.select_obj(conn, 'CALL GET_USER_BY_LOGIN(%s)', (log,))
        if not u:
            raise db_worker.DBException('Пользователь с login = {0} не существует.'.format(log))
            # выбрасываем исключение здесь, а не в db_worker, чтобы показать более информативное сообщение
            # (db_worker не знает, какой был запрос)
        return User(id=u['USER_ID'],
                    login=u['LOGIN'],
                    email=u['EMAIL'],
                    password=u['PASSWORD'],
                    role=u['ROLE'])

    def get_chat_list(self, conn):
        """
        :return: list, содержащий все чаты, в которых устаствует данный пользователь.
        """
        chats = db_worker.select_list(conn, 'CALL GET_CHAT_LIST_BY_USER_ID(%s)', (self.id,))
        return [Chat(id=ch['CHAT_ID'],
                     name=ch['NAME']
                     )
                for ch in chats]

    def get_messages(self, conn):
        """
        :return: list, содержащий все сообщения, отправленные данным пользователем.
        """
        message_list = db_worker.select_list(conn, 'CALL GET_USER_MESSAGES(%s)', (self.id,))
        return [message.Message(id=msg['MESSAGE_ID'],
                                text=msg['MESS_TEXT'],
                                time=msg['SEND_TIME'],
                                chat=Chat(id=msg['CHAT_ID'],
                                          name=msg['CHAT_NAME']),
                                sender=self
                                )
                for msg in message_list]

    def get_last_messages(self, conn, mess_count):
        """
        :return: list, содержащий последние mess_count сообщений, отправленных данным пользователем.
        """
        message_list = db_worker.select_list(conn, 'CALL GET_USER_LAST_MESSAGES(%s, %s)', (self.id, mess_count))
        return [message.Message(id=msg['MESSAGE_ID'],
                                text=msg['MESS_TEXT'],
                                time=msg['SEND_TIME'],
                                chat=Chat(id=msg['CHAT_ID'],
                                          name=msg['CHAT_NAME']),
                                sender=self
                                )
                for msg in message_list]

    def create(self, conn):
        """
        Выполняет сохранение данного пользователя в бд и присвает ему id.
        :exception: db_worker.DBException, если в базе есть пользователь с указанным логином или id.
        """
        self.id = db_worker.insert(conn,
                                   'CALL CREATE_USER(%s, %s, %s, %s)',
                                   (self.login, self.email, self.password, self.role)
                                   )

    @staticmethod
    def delete_user(conn, u):
        """
        Удаляет данного пользователя из бд.
        :exception: db_worker.DBException, если пользователь не сохранён в базе.
        :return: Количество изменённых в бд строк.
        """
        return db_worker.delete(conn, 'CALL DELETE_USER_BY_ID(%s)', (u.id,))


class Chat:
    def __init__(self, name, id=None):
        self.id = id
        self.name = name

    def __str__(self):
        return 'id = {0}, name = {1}'.format(self.id, self.name)

    @staticmethod
    def get_all_chats(conn):
        """
        :return: list, содержащий все чаты
        """
        chats = db_worker.select_list(conn, 'CALL GET_CHATS()')
        return [Chat(id=ch['CHAT_ID'],
                     name=ch['NAME'])
                for ch in chats]

    def get_all_messages(self, conn):
        """
        :return: list, содержащий все сообщения данного чата
        """
        message_list = db_worker.select_list(conn, 'CALL GET_CHAT_MESSAGES(%s)', (self.id,))
        result = []
        for mess in message_list:
            user_id = mess['USER_ID']
            user_sender = User.get_user_by_id(conn, user_id)
            result.append(message.Message(id=mess['MESSAGE_ID'],
                                          time=mess['SEND_TIME'],
                                          text=mess['MESS_TEXT'],
                                          sender=user_sender,
                                          chat=self))
        return result

    def get_last_messages(self, conn, mess_count):
        """
        :return: list, содержащий mess_count последних сообщений данного чата
        """
        message_list = db_worker.select_list(conn, 'CALL GET_LAST_CHAT_MESSAGES(%s, %s)', (self.id, mess_count))
        result = []
        for mess in message_list:
            user_id = mess['USER_ID']
            user_sender = User.get_user_by_id(conn, user_id)
            result.append(message.Message(id=mess['MESSAGE_ID'],
                                          time=mess['SEND_TIME'],
                                          text=mess['MESS_TEXT'],
                                          sender=user_sender,
                                          chat=self))
        return result

    def get_user_list(self, conn):
        """
        :return:
        """
        user_list = db_worker.select_list(conn, 'CALL GET_CHAT_USERS(%s)', (self.id,))
        return [User(id=u['USER_ID'],
                     login=u['LOGIN'],
                     email=u['EMAIL'],
                     password=u['PASSWORD'],
                     role=u['ROLE']
                     )
                for u in user_list]


if __name__ == '__main__':
    db = db_worker.get_db()
    cursor = db.cursor(dictionary=True)

    cursor.close()
    db.close()
    pass
