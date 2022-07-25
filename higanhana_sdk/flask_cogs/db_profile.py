import dataclasses
from flask import Blueprint, request
from higanhana_sdk.db.actualDB import DBProfile, db
from higanhana_sdk.utils.flask import jsonify

bp = Blueprint("profile", __name__)

def profile_get(discord_uid: int):
    profile = DBProfile.query.filter(DBProfile.discord_uid == discord_uid).first()
    if profile is None:
        return jsonify(
            message="No profile found for that discord_uid",
            status_code=404
        )
    return dataclasses.asdict(profile)

def profile_post(discord_uid):
    profile : DBProfile = DBProfile.query.filter(DBProfile.discord_uid == discord_uid).first()
    if profile is None:
        return jsonify(
            message="No profile found for that discord_uid",
            status_code=409
        )
    # merge
    # check target from params or json
    if len(request.json) == 0 and len(request.args) == 0:
        return jsonify(
            message="No data to update",
            status_code=400
        )

    try:
        if len(request.json) > 0:
            profile.updateVars(**request.json)
        else:
            profile.updateVars(**request.args)
        db.session.merge(profile)
        db.session.commit()
        return jsonify(
            message="Profile updated",
            status_code=200,
            success=True
        )
    except:
        return jsonify(
            message="Failed to update profile",
            status_code=409,
            success=False
        )

def profile_put(discord_uid):
    profile : DBProfile = DBProfile.query.filter(DBProfile.discord_uid == discord_uid).first()
    if profile is not None:
        return jsonify(
            message="Profile already exists",
            status_code=409
        )

    if len(request.json) == 0 and len(request.args) == 0:
        return jsonify(
            message="No data to create",
            status_code=400
        )

    try:
        profile = DBProfile(discord_uid=discord_uid)
        if len(request.json) > 0:
            profile.updateVars(**request.json)
        else:
            profile.updateVars(**request.args)
        db.session.add(profile)
        db.session.commit()
        return jsonify(
            message="Profile created",
            status_code=200,
            success=True,
            data=dataclasses.asdict(profile)
        )
    except:
        return jsonify(
            message="Failed to create profile",
            status_code=409,
            success=False
        )

def profile_delete(discord_uid):
    profile : DBProfile = DBProfile.query.filter(DBProfile.discord_uid == discord_uid).first()
    if profile is None:
        return jsonify(
            message="No profile found for that discord_uid",
            status_code=409
        )
    try:
        db.session.delete(profile)
        db.session.commit()
        return jsonify(
            message="Profile deleted",
            status_code=200,
            success=True
        )
    except:
        return jsonify(
            message="Failed to delete profile",
            status_code=409,
            success=False
        )

@bp.route("/<int:discord_uid>", methods=["GET", "POST", "PUT", "DELETE"])
def profile(discord_uid):
    match request.method:
        case "GET":
            return profile_get(discord_uid)
        case "POST":
            return profile_post(discord_uid)
        case "PUT":
            return profile_put(discord_uid)
        case "DELETE":
            return profile_delete(discord_uid)
    return jsonify(
        message="Invalid request method",
        status_code=405
    )


    
