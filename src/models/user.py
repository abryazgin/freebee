import db_worker
import chat
import message


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
        return ('id = {0},\tlogin = {1},\temail = {2},\t' +
                'password = {3},\trole = {4}').format(
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
        :exception: db_worker.DBException,
                    если пользователь с указанным id несуществует
        """
        u = db_worker.select_obj(conn, 'CALL GET_USER_BY_ID(%s)', (id,))
        if not u:
            # выбрасываем исключение здесь, а не в db_worker,
            # чтобы показать более информативное сообщение
            # (db_worker не знает, какой был запрос)
            raise db_worker.DBException(
                'Пользователь с id = {0} не существует.'.format(id)
            )
        return User(id=u['USER_ID'],
                    login=u['LOGIN'],
                    email=u['EMAIL'],
                    password=u['PASSWORD'],
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
                'Пользователь с login = {0} не существует.'.format(log)
            )
        return User(id=u['USER_ID'],
                    login=u['LOGIN'],
                    email=u['EMAIL'],
                    password=u['PASSWORD'],
                    role=u['ROLE'])

    def get_chat_list(self, conn):
        """
        :return: list, содержащий все чаты, в которых
                 участвует данный пользователь.
        """
        chats = db_worker.select_list(
            conn, 'CALL GET_CHAT_LIST_BY_USER_ID(%s)', (self.id,))
        return [chat.Chat(id=ch['CHAT_ID'],
                          name=ch['NAME'])
                for ch in chats]

    def get_messages(self, conn):
        """
        :return: list, содержащий все сообщения,
                 отправленные данным пользователем.
        """
        message_list = db_worker.select_list(
            conn, 'CALL GET_USER_MESSAGES(%s)', (self.id,))
        return [message.Message(id=msg['MESSAGE_ID'],
                                text=msg['MESS_TEXT'],
                                time=msg['SEND_TIME'],
                                chat=chat.Chat(id=msg['CHAT_ID'],
                                name=msg['CHAT_NAME']),
                                sender=self)
                for msg in message_list]

    def get_last_messages(self, conn, mess_count):
        """
        :return: list, содержащий последние mess_count сообщений,
                 отправленных данным пользователем.
        """
        message_list = db_worker.select_list(
            conn, 'CALL GET_USER_LAST_MESSAGES(%s, %s)', (self.id, mess_count))
        return [message.Message(id=msg['MESSAGE_ID'],
                                text=msg['MESS_TEXT'],
                                time=msg['SEND_TIME'],
                                chat=chat.Chat(id=msg['CHAT_ID'],
                                name=msg['CHAT_NAME']),
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

    def update(self, conn, login=None, email=None, password=None, role=None):
        """
        Обновляет данные о пользователе в бд.
        :exception: db_worker.DBException,
                    если новые данные некорректны или
                    пользователь не сохранён в бд.
        :return: Количество изменённых в бд строк.
        """
        # TODO есть ли более элегантный способ проверки параметров?
        login = login if login else self.login
        email = email if email else self.email
        password = password if password else self.password
        role = role if role else self.role

        result = db_worker.update(conn,
                                  'CALL UPDATE_USER(%s, %s, %s, %s, %s)',
                                  (self.id, login, email, password, role))

        self.login = login
        self.email = email
        self.password = password
        self.role = role
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
