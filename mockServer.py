import higanhana_sdk.db.actualDB as actualDB
from higanhana_sdk.utils.flask import setup_flask_cogs
import genshin
import json
from higanhana_sdk.utils.globalConfig import GlobalConfig, CONFIG

genshinClient = genshin.Client()

with open("config.json") as f:
    config = json.load(f)

genshinClient.set_cookies({
    "ltuid" : config["ltuid"],
    "ltoken" : config["ltoken"],
})
        
GlobalConfig(env="hoyovalk").genshinClient = genshinClient

setup_flask_cogs(actualDB.flaskApp, "higanhana_sdk/flask_cogs")
actualDB.flaskApp.run(host="0.0.0.0", port=3000)


