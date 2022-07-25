import dataclasses
from datetime import datetime, timedelta
import typing
from flask import Blueprint
from higanhana_sdk.utils.flask import jsonify
from higanhana_sdk.utils.globalConfig import GlobalConfig
import genshin
from genshin.models import Battlesuit
from higanhana_sdk.db.actualDB import DBHoyovalkCharacterData

bp = Blueprint("hoyovalk", __name__)
config = GlobalConfig(env="hoyovalk")
genshinClient : genshin.GenshinClient = config.genshinClient

LAST_FETCH_DATETIME =  datetime.now() - timedelta(days=1)

async def database_character_data_task(honkai_uid : int, battlesuit_num : int, stigs :typing.List, weapon : typing.Union[list, None]):
    pass

@bp.route("/std/<int:honkai_uid>/<int:battlesuit_number>")
async def std_query(honkai_uid : int, battlesuit_number : int):
    db_entry : DBHoyovalkCharacterData = DBHoyovalkCharacterData.query.filter(DBHoyovalkCharacterData.honkai_uid_character == f"{honkai_uid}-{battlesuit_number}").first()
    if db_entry is not None and db_entry.fetched_time + timedelta(hours=1) >= datetime.now():
        return jsonify(
            data=dataclasses.asdict(db_entry),
            status_code=200,
            success=True,
            fetched_from="db"
        )

    try:
        queryed_battlesuits = await genshinClient.get_honkai_battlesuits(honkai_uid)
    except:
        return jsonify(
            message="error fetching data",
            status_code=404,
            success=False,
        )

    if queryed_battlesuits is None or len(queryed_battlesuits) == 0:
        return jsonify(
            message="No data found",
            status_code=404,
            stage = "search",
            success=False
        )

    interested_bs = None
    for bs in queryed_battlesuits:
        bs : Battlesuit
        if bs.id == battlesuit_number:
            interested_bs = bs
            break

    if interested_bs is None:
        return jsonify(
            message="No data found",
            status_code=404,
            stage = "filter",
            success=False
        )

    weapon = interested_bs.weapon
    if weapon is not None:
        weapon = [
            interested_bs.weapon.id, 
            interested_bs.weapon.name, 
            interested_bs.weapon.icon
        ]

    stigs = [None, None, None]
    stigs = [
        [x.name, x.id, x.rarity, x.icon]
        for x in interested_bs.stigmata
    ],


    lastData = jsonify(
        message="Data found",
        status_code=200,
        success=True,
        valk_name= interested_bs.name,
        honkai_uid=honkai_uid,
        battlesuit_number=battlesuit_number,
        stigs=stigs,
        weapons=weapon,
    )

    return lastData

    


    







