import genshin
import unittest
import json
from flask import Flask

class t_genshin(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.genshinClient = genshin.GenshinClient()

        with open("config.json") as f:
            self.config = json.load(f)

        self.genshinClient.set_cookies({
            "ltuid" : self.config["ltuid"],
            "ltoken" : self.config["ltoken"],
        })
        

    async def test_genshin_1(self):
        await self.hv.getCharacters(104373522)
        pass
    

