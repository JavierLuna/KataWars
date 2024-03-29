from flask import Flask
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

from config import config

db = SQLAlchemy()
ma = Marshmallow()


def create_app(config_name='default'):
    app = Flask(__name__, static_folder='./static')
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # Plugins initialization goes here
    db.init_app(app)
    ma.init_app(app)

    from .api import api_v1 as api_v1_blueprint
    app.register_blueprint(api_v1_blueprint, url_prefix='/api')

    return app
