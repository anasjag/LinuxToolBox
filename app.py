import os
from flask import Flask
from pymongo import MongoClient
from dotenv import load_dotenv
# import certifi

load_dotenv()

SECRET_KEY = os.urandom(32)

from routes import pages


def create_app():
    app = Flask(__name__)
    # client = MongoClient(os.getenv("MONGODB_URI"))
    app.config["MONGODB_URI"] = os.environ.get("MONGODB_URI")
    app.config["MONGODB_DB"] = os.environ.get("MONGODB_DB")
    # , tlsCAFile=certifi.where()
    app.db = MongoClient(app.config["MONGODB_URI"])[
        app.config.get("MONGODB_DB")
    ]
    app.config["SECRET_KEY"] = SECRET_KEY
    # app.db = client.LinuxToolBox
    # 6eez
    app.register_blueprint(pages)

    return app
