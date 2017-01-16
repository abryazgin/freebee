import unittest
import user
import db_worker


class TestUser(unittest.TestCase):
    def setUp(self):
        self.db = db_worker.get_db()
        self.cursor = self.db.cursor(dictionary=True)

    def tearDown(self):
        self.cursor.close()
        self.db.close()

    def test_read_admin(self):
        u = user.User.get_user_by_login(self.cursor, 'admin')
        self.assertEqual(u.id, 1)

    def test_read_nonsense(self):
        u = user.User.get_user_by_login(self.cursor, 'sdd13##@@!rhrue!@')
        self.assertIsNone(u)


if __name__ == '__main__':
    unittest.main()
