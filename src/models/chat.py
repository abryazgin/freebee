from . import db_worker
from . import ModelFactory


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
        message_list = db_worker.select_list(
            conn, 'CALL GET_CHAT_MESSAGES(%s)', (self.id,))
        result = []
        for mess in message_list:
            user_id = mess['USER_ID']
            user_sender = ModelFactory.User.get_user_by_id(conn, user_id)
            result.append(ModelFactory.Message(id=mess['MESSAGE_ID'],
                                  time=mess['SEND_TIME'],
                                  text=mess['MESS_TEXT'],
                                  sender=user_sender,
                                  chat=self))
        return result

    def get_last_messages(self, conn, mess_count):
        """
        :return: list, содержащий mess_count последних сообщений данного чата
        """
        message_list = db_worker.select_list(
            conn, 'CALL GET_LAST_CHAT_MESSAGES(%s, %s)', (self.id, mess_count))
        result = []
        for mess in message_list:
            user_id = mess['USER_ID']
            user_sender = ModelFactory.User.get_user_by_id(conn, user_id)
            result.append(ModelFactory.Message(id=mess['MESSAGE_ID'],
                                               time=mess['SEND_TIME'],
                                               text=mess['MESS_TEXT'],
                                               sender=user_sender,
                                               chat=self))
        return result

    def get_user_list(self, conn):
        """
        :return: list, содержащий всех пользователей в данном чате.
        """
        user_list = db_worker.select_list(
            conn, 'CALL GET_CHAT_USERS(%s)', (self.id,))
        return [ModelFactory.User(id=u['USER_ID'],
                                  login=u['LOGIN'],
                                  email=u['EMAIL'],
                                  password=u['PASSWORD'],
                                  role=u['ROLE'])
                for u in user_list]

    def create(self, conn):
        """
        Выполняет сохранение данного чата в бд и присвает ему id.
        """
        self.id = db_worker.insert(conn, 'CALL CREATE_CHAT(%s)', (self.name,))

    @staticmethod
    def delete(conn, ch):
        """
        Удаляет данный чат из бд.
        :exception: db_worker.DBException, если чат не сохранён в базе.
        :return: Количество изменённых в бд строк.
        """
        return db_worker.delete(conn, 'CALL DELETE_CHAT_BY_ID(%s)', (ch.id,))

    def update(self, conn, name):
        """
        Обновляет данные о чате в бд.
        :exception: db_worker.DBException, если чат не сохранён в бд.
        :return: Количество изменённых в бд строк.
        """
        result = db_worker.update(
            conn, 'CALL UPDATE_CHAT(%s, %s)', (self.id, name))
        self.name = name
        return result

    def add_user(self, conn, us):
        """
        Добавляет пользователя в чат.
        :exception: db_worker.DBException,
                    если чат/пользователь не сохранены в бд
                    или пользователь уже добавлен в чат.
        :return: Количество изменённых в бд строк.
        """
        return db_worker.update(
            conn, 'CALL ADD_USER_IN_CHAT(%s, %s)', (self.id, us.id))

    def remove_user(self, conn, us):
        """
        Удаляет пользователя из чат.
        :exception: db_worker.DBException,
                    если чат/пользователь не сохранены в бд
                    или пользователь не входит в чат.
        :return: Количество изменённых в бд строк.
        """
        return db_worker.update(
            conn, 'CALL REMOVE_USER_FROM_CHAT(%s, %s)', (us.id, self.id))


if __name__ == '__main__':
    db = db_worker.get_db()
    cursor = db.cursor(dictionary=True)

    cursor.close()
    db.close()
