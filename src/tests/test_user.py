import unittest
from models import user
from models import db_worker


class TestUser(unittest.TestCase):
    #TODO продумать автоматическую инициализацию тестовых данных
    """
    Тесты корректно работают только на данных, формируемыми скриптами из sql/re_init_db
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

    def test_double_user_login(self):
        new_user = user.User(login='admin',
                             email='dtfyguhijokm',
                             password='skip',
                             role=user.User.CLIENT
                             )
        self.assertRaises(db_worker.DBException,
                          new_user.create,
                          self.cursor
                          )

    def test_double_user_email(self):
        new_user = user.User(login='dtfyguhijokm',
                             email='smth1@ex.com',
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
        messages_list = u.get_messages(self.cursor)
        self.assertEqual(2, len(messages_list))

    def test_admin_last_message(self):
        u = user.User(id=1,
                      login='admin',
                      email='smth1@ex.com',
                      password='admpass',
                      role=user.User.ADMIN)
        messcnt = 1
        messages_list = u.get_last_messages(self.cursor, messcnt)
        self.assertEqual(messcnt, len(messages_list))

    # bdd test
    @unittest.skip('not implemented yet')
    def test_case(self):
        # login = generator.get_random_login()
        # role = User.ADMIN
        pass
        # create user
        # get user - assert exists, assert attr in db eq inserted attr
        # delete
        # get user - assert not exists


if __name__ == '__main__':
    unittest.main(verbosity=2)
