from flask import current_app as app, Response
from models import db, Startup
import json as json
import services


@app.route('/update', methods=['GET'])
def update_records():
    response = services.request_data()
    if response["result"] == "OK" and "data" in response:
        services.parse_data(response["data"])
    else:
        return response
    resp = Response(json.dumps({"status": "OK"}))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Content-Type'] = 'application/json'
    return resp


@app.route('/', methods=['GET'])
def list_records():
    startups = [x.as_dict() for x in Startup.query.all()]
    resp = Response(json.dumps({"startups": startups}))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Content-Type'] = 'application/json'
    return resp
