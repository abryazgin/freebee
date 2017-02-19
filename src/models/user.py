from . import db_worker
from . import ModelFactory


class User:
    ADMIN = 'admin'
    STAFFER = 'staffer'
    CLIENT = 'client'

    def __init__(self, login, email, role, password, enable=True, id=None):
        self.id = id
        self.login = login
        self.email = email
        self.password = password
        self.role = role
        self.enable = enable

    def __str__(self):
        return ('id = {0},\tlogin = {1},\temail = {2},\t' +
                'password = {3},\trole = {4},\tenable = {5}').format(
            self.id, self.login, self.email, self.password,
            self.role, self.enable)

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
                     enable=u['USER_ENABLE'],
                     role=u['ROLE'])
                for u in users]

    @staticmethod
    def get_user_by_id(conn, id):
        """
        :exception: db_worker.DBException,
                    если пользователь с указанным id несуществует
        """
        u = db_worker.select_obj(conn, 'CALL GET_USER_BY_ID(%s)', (id,))
        if not u:
            # выбрасываем исключение здесь, а не в db_worker,
            # чтобы показать более информативное сообщение
            # (db_worker не знает, какой был запрос)
            raise db_worker.DBException(
                'Пользователь с id = {0} не существует.'.format(id))
        return User(id=u['USER_ID'],
                    login=u['LOGIN'],
                    email=u['EMAIL'],
                    password=u['PASSWORD'],
                    enable=u['USER_ENABLE'],
                    role=u['ROLE'])

    @staticmethod
    def get_user_by_login(conn, log):
        """
        :exception: db_worker.DBException,
                    если пользователь с указанным логином несуществует
        """
        u = db_worker.select_obj(conn, 'CALL GET_USER_BY_LOGIN(%s)', (log,))
        if not u:
            # выбрасываем исключение здесь, а не в db_worker,
            # чтобы показать более информативное сообщение
            # (db_worker не знает, какой был запрос)
            raise db_worker.DBException(
                'Пользователь с login = {0} не существует.'.format(log))
        return User(
            id=u['USER_ID'],
            login=u['LOGIN'],
            email=u['EMAIL'],
            password=u['PASSWORD'],
            enable=u['USER_ENABLE'],
            role=u['ROLE']
        )

    def get_chat_list(self, conn):
        """
        :return: list, содержащий все чаты, в которых
                 участвует данный пользователь.
        """
        chats = db_worker.select_list(
            conn, 'CALL GET_CHAT_LIST_BY_USER_ID(%s)', (self.id,))
        return [ModelFactory.Chat(id=ch['CHAT_ID'],
                                  enable=ch['CHAT_ENABLE'],
                                  name=ch['NAME'])
                for ch in chats]

    def get_messages(self, conn):
        """
        :return: list, содержащий все сообщения,
                 отправленные данным пользователем.
        """
        message_list = db_worker.select_list(
            conn, 'CALL GET_USER_MESSAGES(%s)', (self.id,))
        return [ModelFactory.Message(
            id=msg['MESSAGE_ID'],
            text=msg['MESS_TEXT'],
            time=msg['SEND_TIME'],
            chat=ModelFactory.Chat(
                id=msg['CHAT_ID'],
                enable=msg['CHAT_ENABLE'],
                name=msg['CHAT_NAME']),
            enable=msg['MESS_ENABLE'],
            sender=self)
            for msg in message_list]

    def get_last_messages(self, conn, mess_count):
        """
        :return: list, содержащий последние mess_count сообщений,
                 отправленных данным пользователем.
        """
        message_list = db_worker.select_list(
            conn, 'CALL GET_USER_LAST_MESSAGES(%s, %s)', (self.id, mess_count))
        return [ModelFactory.Message(
            id=msg['MESSAGE_ID'],
            text=msg['MESS_TEXT'],
            time=msg['SEND_TIME'],
            chat=ModelFactory.Chat(id=msg['CHAT_ID'],
                                   enable=msg['CHAT_ENABLE'],
                                   name=msg['CHAT_NAME']),
            enable=msg['MESS_ENABLE'],
            sender=self)
            for msg in message_list]

    def create(self, conn):
        """
        Выполняет сохранение данного пользователя в бд и присвает ему id.
        :exception: db_worker.DBException,
                    если в базе есть пользователь с указанным логином или id.
        """
        self.id = db_worker.insert(
            conn,
            'CALL CREATE_USER(%s, %s, %s, %s)',
            (self.login, self.email, self.password, self.role))

    def update(self, conn):
        """
        Обновляет данные о пользователе в бд.
        :exception: db_worker.DBException,
                    если новые данные некорректны или
                    пользователь не сохранён в бд.
        :return: Количество изменённых в бд строк.
        """
        result = db_worker.update(conn,
                                  'CALL UPDATE_USER(%s, %s, %s, %s, %s, %s)',
                                  (self.id, self.login, self.email,
                                   self.password, self.role, self.enable))
        return result

    @staticmethod
    def delete(conn, u):
        """
        Удаляет данного пользователя из бд.
        :exception: db_worker.DBException,
                    если пользователь не сохранён в базе.
        :return: Количество изменённых в бд строк.
        """
        return db_worker.delete(conn, 'CALL DELETE_USER_BY_ID(%s)', (u.id,))


if __name__ == '__main__':
    db = db_worker.get_db()
    cursor = db.cursor(dictionary=True)

    cursor.close()
    db.close()
