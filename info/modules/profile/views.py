import time

from flask import request, render_template, jsonify, current_app, make_response
from info.utils.browser_get_profile import browser_start
import json

from . import profile_blu
from info import redis_store


@profile_blu.route("/profile", methods=['GET', 'POST'])
def get_profile():
    if request.method == "GET":
        return render_template('profile.html', my_dict=None)
    recv_data = request.get_data()
    account = recv_data.decode()

    data = redis_store.get("ProfileID_" + account)
    print(data)
    if data is not None:
        data = json.loads(data)
        code = 200
        if data == "no activity to share.":
            code = 300
        if data == "Query failed":
            code = 400
        life_time = time.time() + 1800
        response = make_response(jsonify({"code": code, "msg": data, }))
        response.set_cookie('profile_id', account, expires=life_time)
        return response

    data = browser_start(account)

    code = 200
    if data == "no activity to share.":
        code = 300
    if data == "Query failed":
        code = 400
    if code == 200 or code == 300:
        try:
            redis_store.set("ProfileID_" + account, json.dumps(data), 1800)
        except Exception as e:
            current_app.logger.error(e)

    response = make_response(jsonify({"code": code, "msg": data, }))
    life_time = time.time() + 1800
    response.set_cookie('profile_id', account, expires=life_time)
    return response


@profile_blu.route("/profile_num", methods=['GET'])
def get_profile_num():
    account = request.cookies.get("profile_id")

    try:
        data = redis_store.get("ProfileID_" + account)
    except:
        return render_template("404.html")

    my_dict = json.loads(data).get("m_dict")

    return render_template('profile_num.html', my_dict=my_dict)
