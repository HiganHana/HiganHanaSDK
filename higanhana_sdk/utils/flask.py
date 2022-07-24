from flask import Flask, Blueprint
import inspect
import os
import importlib

def setup_flask_cogs(flaskApp : Flask, string : str) -> None:

    # import all blueprints
    for file in os.listdir(string):
        if file.endswith(".py") and not file.startswith("_"):
            mod = importlib.import_module(f"{string.replace('/','.')}.{file[:-3]}")
            for name, obj in inspect.getmembers(mod):
                if isinstance(obj, Blueprint):
                    flaskApp.register_blueprint(obj, url_prefix=f"/{obj.name}/")


def jsonify(message :str, status_code : int = 200, **kwargs) -> dict:
    return {"message": message, "status_code": status_code, **kwargs}
    