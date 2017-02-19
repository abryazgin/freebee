from . import db_worker


class Message:
    def __init__(self, time, text, sender, chat, enable=True, id=None):
        self.id = id
        self.sender = sender
        self.time = time
        self.text = text
        self.chat = chat
        self.enable = enable

    def __str__(self):
        return ('id = {0}, sender.login = {1}, chat.name = {2}, ' +
                'time = {3}, text = {4}').format(
            self.id, self.sender.login, self.chat.name,
            self.time, self.text)

    def create(self, conn):
        """
        Выполняет сохранение данного чата в бд и присвает ему id.
        """
        self.id = db_worker.insert(
            conn,
            'CALL CREATE_MESSAGE(%s, %s, %s, %s, %s)',
            (self.sender.id, self.chat.id, self.time, self.text, self.enable))

    @staticmethod
    def delete(conn, mess):
        """
        Удаляет сообщение из бд.
        :exception: db_worker.DBException, если сообщение не сохранено в базе.
        :return: Количество изменённых в бд строк.
        """
        return db_worker.delete(
            conn, 'CALL DELETE_MESSAGE_BY_ID(%s)', (mess.id,))

    def update(self, conn):
        """
        Обновляет данные о сообщение в бд.
        :exception: db_worker.DBException,
                    если новые данные некорректны или
                    сообщение не сохранено в бд.
        :return: Количество изменённых в бд строк.
        """
        result = db_worker.update(
            conn,
            'CALL UPDATE_MESSAGE(%s, %s, %s, %s, %s, %s)',
            (self.id, self.sender.id, self.chat.id, self.time,
             self.text, self.enable))
        return result


if __name__ == '__main__':
    db = db_worker.get_db()
    cursor = db.cursor(dictionary=True)

    cursor.close()
    db.close()
