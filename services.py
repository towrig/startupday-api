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
            industry=parse_industries(x["answers"]["industries"])
        )
        print('Startup added: ' + name)
        db.session.add(startup)

    db.session.commit()

