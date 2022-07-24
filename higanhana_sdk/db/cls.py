from dataclasses import dataclass
import typing

from higanhana_sdk.db.clsi import DBClsInterface

@dataclass
class Profile(DBClsInterface):
    discord_uid : int = None
    honkai_uid  : int = None
    genshin_uid : int = None
    honkai_guild_intent : typing.Literal["INTEND_TO_JOIN", "JOINED", "LEFT", None] = None

@dataclass
class UserTag(DBClsInterface):
    tag : str
    discord_uid : int

@dataclass
class HoyovalkImageCache(DBClsInterface):
    id : int
    cache : bytes

@dataclass
class HoyovalkCombinedCache(DBClsInterface):
    uid : int
    weapon : int
    stigT : int
    stigM : int
    stigB : int
    cache : bytes
