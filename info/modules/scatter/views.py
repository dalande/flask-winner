# encoding=utf-8

import json

from info import redis_store
from . import scatter_blu
from flask import request, render_template, jsonify, current_app
from info.utils.kw_scatter import Scatter


@scatter_blu.route("/scatter", methods=["GET", "POST"])
def get_scatter():
    if request.method == "GET":
        return render_template("scatter.html")

    recv_data = request.get_data()
    keywords = recv_data.decode()
    data = redis_store.get("keywords_" + keywords)
    if data is not None:
        data = json.loads(data)
        return jsonify({"code": 200, "msg": data, })

    s = Scatter(keywords, "us")
    data = s.create_scatter_data()
    print(data)

    if data is None:
        return jsonify({"code": 400, "msg": "页面抓取失败", })

    try:
        redis_store.set("keywords_" + keywords, json.dumps(data), 1800)
    except Exception as e:
        current_app.logger.error(e)

    return jsonify({"code": 200, "msg": data, })


@scatter_blu.route("/kw_history", methods=["GET", "POST"])
def kw_history():
    if request.method == "GET":
        data = "chair"
        return jsonify({"code": 200, "msg": data, })
