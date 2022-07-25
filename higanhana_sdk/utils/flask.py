from pprint import pformat
from flask import Flask, Blueprint
import inspect
import os
import importlib
from flask import make_response
from json import dumps

def setup_flask_cogs(flaskApp : Flask, string : str) -> None:

    # import all blueprints
    for file in os.listdir(string):
        if file.endswith(".py") and not file.startswith("_"):
            mod = importlib.import_module(f"{string.replace('/','.')}.{file[:-3]}")
            for name, obj in inspect.getmembers(mod):
                if isinstance(obj, Blueprint):
                    flaskApp.register_blueprint(obj, url_prefix=f"/{obj.name}/")


def jsonify(status=200, indent=4, sort_keys=True, **kwargs):
    response = make_response(dumps(dict(**kwargs), indent=indent, sort_keys=sort_keys))
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    response.headers['mimetype'] = 'application/json'
    response.status_code = status
    return response