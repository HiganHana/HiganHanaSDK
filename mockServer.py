import higanhana_sdk.db.actualDB as actualDB
from higanhana_sdk.utils.flask import setup_flask_cogs

setup_flask_cogs(actualDB.flaskApp, "higanhana_sdk/dbFlaskCogs")
actualDB.flaskApp.run(host="0.0.0.0", port=3000)


