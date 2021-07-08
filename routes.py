from flask import current_app as app, Response, request
from models import db, Startup
import json as json
import services


@app.route('/update', methods=['GET'])
def update_records():
    response = services.request_data()
    if response is not None and isinstance(response, list):
        services.parse_data(response)
    else:
        return response
    resp = Response(json.dumps({"status": "OK"}))
    resp.headers['Content-Type'] = 'application/json'
    return resp


@app.route('/', methods=['GET'])
def list_records():
    industry = request.args.get('industry', default="", type=str)
    stage = request.args.get('stage', default="", type=str)

    #filtered = filter(lambda score: score >= 70, scores)

    startups = [x.as_dict() for x in Startup.query.all()]
    resp = Response(json.dumps({"startups": startups}))
    resp.headers['Content-Type'] = 'application/json'
    return resp
