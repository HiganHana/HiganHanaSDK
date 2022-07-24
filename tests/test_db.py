import os
import unittest

class t_db(unittest.TestCase):
    def test_db_init(self):
        import higanhana_sdk.db.actualDB
        self.assertTrue(os.path.exists(os.path.join(os.getcwd(), "data", "server.db")))
        self.assertTrue(os.path.exists(os.path.join(os.getcwd(), "data", "hoyovalk.db")))