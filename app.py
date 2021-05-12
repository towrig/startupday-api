import os

from flask import Flask
import db

basedir = os.path.abspath(os.path.dirname(__file__))

def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'sqlite'),
    )

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