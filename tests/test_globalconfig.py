import unittest

from higanhana_sdk.utils.globalConfig import CONFIG, GlobalConfig

class t_globalconfig(unittest.TestCase):
    def test(self):
        CONFIG.x = 2
        CONFIG.y = 3
        CONFIG.not_serializable = GlobalConfig
        self.assertEqual(CONFIG.x, 2)
        self.assertEqual(CONFIG.y, 3)
        CONFIG2 = GlobalConfig(env="hello")
        CONFIG2.x = 1
        self.assertEqual(CONFIG2.x, 1)
        self.assertEqual(CONFIG2.y, 3)
        
        data = CONFIG._serializeScope()
        self.assertEqual(data, {'x': 2, 'y': 3})
        data2 = CONFIG2._serializeScope()
        self.assertEqual(data2, {'x': 1})

        pass
