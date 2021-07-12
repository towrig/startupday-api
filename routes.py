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
    stage = request.args.get('stage', default="", type=str)
    industry = request.args.get('industry', default="", type=str)
    country = request.args.get('country', default="", type=str)

    if stage != "":
        startups = services.filter_by_stage(stage)
    else:
        startups = [x.as_dict() for x in Startup.query.all()]

    if industry != "":
        startups = [x for x in startups if industry in x["industry"].split(",")]

    if country != "":
        startups = [x for x in startups if x["country"] == country]

    resp = Response(json.dumps({
        "startups": startups,
        "industries": services.get_industries(),
        "stages": services.get_stages(),
        "countries": services.get_countries()
    }))
    resp.headers['Content-Type'] = 'application/json'
    return resp
