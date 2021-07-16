from apscheduler.schedulers.background import BackgroundScheduler


def update_task(app):
    print("--UPDATING RECORDS...--")
    with app.app_context():
        from services import request_data, parse_data
        response = request_data()

        if response is not None and isinstance(response, list):
            parse_data(response)
        else:
            print("--UPDATE FAILED--")

        print("--UPDATED RECORDS SUCCESSFULLY!--")


def init(app):
    sched = BackgroundScheduler(daemon=True)
    sched.add_job(lambda: update_task(app), 'interval', hours=2)
    update_task(app)
    sched.start()
