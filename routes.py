from flask import request, render_template, make_response
from datetime import datetime as dt
from flask import current_app as app
from .models import db, Startup
import requests
import json as json


def startup_exists(name):
    # print("\n"+name+" results:")
    # print(db.session.query(Startup.id).filter_by(name=name).first())
    return db.session.query(Startup.id).filter_by(name=name).first() is not None


def consented(item):
    if "answers" not in item["company"]:
        return False
    return item["company"]["answers"]["startupday2021_consent"]["data"] == "true"


def parse_industries(arr):
    result = ""
    for row in arr:
        result += row + ","
    return result[:-1]


def parse_data(data):
    for x in data:
        if not consented(x):
            continue

        info = x["company"]
        name = info["name"]

        if not startup_exists(name):
            logo = ""
            if info["logo"] is not None:
                logo = info["logo"]["url"]
            startup = Startup(
                name=name,
                logo=logo,
                oneliner=info["answers"]["oneliner"]["data"],
                stage=info["answers"]["company_stage"]["data"],
                industry=parse_industries(info["answers"]["industries"]["data"])
            )
            print('Startup added: ' + name)
            db.session.add(startup)

    db.session.commit()


@app.route('/update', methods=['GET'])
def update_records():
    """Create a user via query string parameters."""
    headers = {'X-Access-Token': 'xrlc3k7pm9p3zycfn2kwxz5xjbw8xe0r7kfocpeniclwdqkybc9o35x4zssulhpi99233'}
    x = requests.get('https://startupincluder.com/api/dealrooms/4437/applications', headers=headers).content
    response = json.loads(x)

    if response["result"] == "OK" and "data" in response:
        parse_data(response["data"])
    else:
        return response

    return {"status": "OK"}


@app.route('/', methods=['GET'])
def list_records():
    startups = [x.as_dict() for x in Startup.query.all()]

    return json.dumps({"startups": startups})
