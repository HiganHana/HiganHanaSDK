import unittest
from unittest.mock import patch
from higanhana_sdk.db.actualDB import DBProfile, db
import requests

class t_flask_server(unittest.TestCase):

    def setUp(self) -> None:
        self.profile = DBProfile(discord_uid=1, honkai_uid=1, genshin_uid=1)
        db.session.merge(self.profile)
        db.session.commit()

    def test_flask_profile_get(self):
        r = requests.get("http://localhost:3000/profile/1")
        self.assertEqual(r.status_code, 200)
        self.assertIn("discord_uid", r.json())
        self.assertIn("honkai_uid", r.json())
        self.assertIn("genshin_uid", r.json())
        self.assertIn("honkai_guild_intent", r.json())

        self.assertEqual(r.json()["discord_uid"], 1)
        self.assertEqual(r.json()["honkai_uid"], 1)
        self.assertEqual(r.json()["genshin_uid"], 1)
        self.assertEqual(r.json()["honkai_guild_intent"], None)
        
    def test_flask_profile_post(self):
        r = requests.post("http://localhost:3000/profile/1", json={"honkai_guild_intent": "INTEND_TO_JOIN"})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["message"], "Profile updated")
        self.assertEqual(r.json()["success"], True)

        r = requests.get("http://localhost:3000/profile/1")
        self.assertEqual(r.json()["honkai_guild_intent"], "INTEND_TO_JOIN")


    