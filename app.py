import os

from flask import Flask
import db

basedir = os.path.abspath(os.path.dirname(__file__))

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    db.init_app(app)

    @app.route("/api")
    def api():
        return {
            "status": "OK",
            "msg": "DATA HERE",
        }

    @app.errorhandler(404)
    def not_found(error):
        return {
            "status": "ERROR",
            "msg": "Endpoint does not exist",
        }

    return app