from dataclasses import dataclass
import os
from higanhana_sdk.db.cls import Profile, HoyovalkImageCache, HoyovalkCombinedCache, UserTag
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

workplaceFolder = os.getcwd()
dataFolder = os.path.join(workplaceFolder, "data")
os.makedirs(dataFolder, exist_ok=True)

flaskApp = Flask(__name__)
flaskApp.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{dataFolder}/server.db"
flaskApp.config["SQLALCHEMY_BINDS"] = {
    "hoyovalk" : f"sqlite:///{dataFolder}/hoyovalk.db",
}
flaskApp.config['SQLALCHEMY_ECHO'] = True
flaskApp.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(flaskApp)

@dataclass
class DBProfile(Profile, db.Model):
    __tablename__ = "profile"
    discord_uid = db.Column(db.Integer, primary_key=True)
    honkai_uid = db.Column(db.Integer)
    genshin_uid = db.Column(db.Integer)
    honkai_guild_intent = db.Column(db.Enum("INTEND_TO_JOIN", "JOINED", "LEFT"), default=None)

@dataclass
class DBUserTag(UserTag, db.Model):
    __tablename__ = "user_tag"
    tag = db.Column(db.String(255), primary_key=True)
    discord_uid = db.Column(db.Integer)

@dataclass
class DBHoyovalkImageCache(HoyovalkImageCache, db.Model):
    __tablename__ = "image_cache"
    __bind_key__ = "hoyovalk"
    id = db.Column(db.Integer, primary_key=True)
    cache = db.Column(db.LargeBinary)

@dataclass
class DBHoyovalkCombinedCache(HoyovalkCombinedCache, db.Model):
    __tablename__ = "combined_cache"
    __bind_key__ = "hoyovalk"
    uid = db.Column(db.Integer, primary_key=True)
    weapon = db.Column(db.Integer)
    stigT = db.Column(db.Integer)
    stigM = db.Column(db.Integer)
    stigB = db.Column(db.Integer)
    cache = db.Column(db.LargeBinary)

db.create_all()