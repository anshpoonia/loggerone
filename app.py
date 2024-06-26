from flask import Flask, render_template, request, jsonify, abort
from flask_cors import CORS, cross_origin
from time import time
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

client = MongoClient("localhost", 27017, server_api=ServerApi('1'))
db = client.speakup
LOG = db["log"]

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

allowable_gap = 1.0


def check(rid):
    timestamp = time()

    doc = LOG.find_one({"_id": rid})
    if isinstance(doc, dict):
        if timestamp - doc["timestamp"] < allowable_gap:
            LOG.update_one({"_id": rid}, {"$inc": {"reject": 1}})
            return False
        LOG.update_one({"_id": rid}, {"$set": {"timestamp": timestamp}, "$inc": {"success": 1}})
        return True
    LOG.insert_one({
        "_id": rid,
        "timestamp": timestamp,
        "success": 1,
        "reject": 0
    })
    return True


@app.route('/')
def home_handler():
    return render_template("index.html")


@app.route('/request', methods=["POST"])
@cross_origin()
def request_handler():
    rid = request.json.get("location")
    if check(rid):
        return jsonify({"code": "OK"})

    res = jsonify({"code": "Rejected"})
    res.status = 500
    return abort(res)


@app.route('/set', methods=["POST"])
@cross_origin()
def time_set_handler():
    try:
        global allowable_gap
        allowable_gap = int(request.json.get("time")) / 1000.0
        return jsonify({"code": "OK"})
    except ValueError:
        return jsonify({"code": "Incorrect value"})


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)
