import unittest
from models import user
from models import db_worker


class TestUser(unittest.TestCase):
    # TODO продумать автоматическую инициализацию тестовых данных
    """
    Тесты корректно работают только на данных,
    формируемых скриптами из sql/re_init_db
    """
    def setUp(self):
        self.db = db_worker.get_db()
        self.cursor = self.db.cursor(dictionary=True)

    def tearDown(self):
        self.cursor.close()
        self.db.close()

    def test_read_admin_by_login(self):
        u = user.User.get_user_by_login(self.cursor, 'admin')
        self.assertEqual(u.id, 1)

    def test_read_admin_by_id(self):
        u = user.User.get_user_by_id(self.cursor, 1)
        self.assertEqual(u.login, 'admin')

    def test_read_nonsense(self):
        self.assertRaises(db_worker.DBException,
                          user.User.get_user_by_login,
                          self.cursor,
                          'sdd13##@@!rhrue!@'
                          )

    def test_select_all(self):
        user_list = user.User.get_all_users(self.cursor)
        self.assertEqual(6, len(user_list))

    def test_user_create_not_unique(self):
        new_user = user.User(login='dtfyguhijokm',
                             email='smth1@ex.com',
                             password='skip',
                             role=user.User.CLIENT
                             )
        self.assertRaises(db_worker.DBException,
                          new_user.create,
                          self.cursor
                          )
        new_user = user.User(login='admin',
                             email='dtfyguhijokm',
                             password='skip',
                             role=user.User.CLIENT
                             )
        self.assertRaises(db_worker.DBException,
                          new_user.create,
                          self.cursor
                          )

    def test_user_chat_count(self):
        admin = user.User(id=1,
                          login='admin',
                          email='smth1@ex.com',
                          role=user.User.ADMIN,
                          password='admpass'
                          )
        chat_list_admin = admin.get_chat_list(self.cursor)
        self.assertEqual(1, len(chat_list_admin))

    def test_notexist_user_chat_count(self):
        notexist_user = user.User(id=-99999,
                                  login='admin',
                                  email='smth1@ex.com',
                                  role=user.User.ADMIN,
                                  password='admpass'
                                  )
        chat_list = notexist_user .get_chat_list(self.cursor)
        self.assertEqual(0, len(chat_list))

    def test_admin_message(self):
        u = user.User(id=1,
                      login='admin',
                      email='smth1@ex.com',
                      password='admpass',
                      role=user.User.ADMIN)
        messages_list = u.get_all_messages(self.cursor)
        self.assertEqual(2, len(messages_list))
        messages_list = u.get_messages_slice(self.cursor, begin=0, limit=1)
        self.assertEqual(1, len(messages_list))
        messages_list = u.get_last_messages(self.cursor, limit=1)
        self.assertEqual(1, len(messages_list))

    def test_user_update_not_unique(self):
        u = user.User(id=1,
                      login='admin',
                      email='smth1@ex.com',
                      password='admpass',
                      role=user.User.ADMIN)
        u.login = 'paul'
        self.assertRaises(db_worker.DBException,
                          u.update,
                          conn=self.cursor)
        u.login = 'admin'
        u.email = 'smth2@ex.com'
        self.assertRaises(db_worker.DBException,
                          u.update,
                          conn=self.cursor)


if __name__ == '__main__':
    unittest.main(verbosity=2)
