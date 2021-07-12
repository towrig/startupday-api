from models import db, Startup
import requests
import json as json

def request_data():
    headers = {'X-Access-Token': 'xrlc3k7pm9p3zycfn2kwxz5xjbw8xe0r7kfocpeniclwdqkybc9o35x4zssulhpi99233'}
    x = requests.get('https://app.dealum.com/api/integrations/dealrooms/4437/applications', headers=headers).content
    return json.loads(x)

def startup_exists(name):
    return db.session.query(Startup.id).filter_by(name=name).first() is not None


def consented(item):
    if "answers" not in item:
        return False
    return item["answers"]["startupday2021_consent"] == "Yes"


def parse_industries(arr):
    result = ""
    for row in arr:
        result += row + ","
    return result[:-1]

def parse_data(data):

    Startup.query.delete()
    for x in data:
        if not consented(x):
            continue

        name = x["name"]
        logo = ""
        if "logo" in x:
            logo = x["logo"]
        startup = Startup(
            name=name,
            logo=logo,
            oneliner=x["answers"]["oneliner"],
            stage=x["answers"]["company_stage"],
            industry=parse_industries(x["answers"]["industries"]),
            country=x["answers"]["country"]
        )
        db.session.add(startup)

    db.session.commit()


def filter_by_stage(stage):
    return [x.as_dict() for x in Startup.query.filter(Startup.stage.is_(stage)).all()]


def get_industries():
    results = Startup.query.with_entities(Startup.industry).all()
    result_list = []

    for x in results:
        for i in x[0].split(","):
            if i not in result_list:
                result_list.append(i.strip())

    return result_list


def get_stages():
    results = Startup.query.with_entities(Startup.stage).distinct(Startup.stage).all()
    return [x[0] for x in results]

