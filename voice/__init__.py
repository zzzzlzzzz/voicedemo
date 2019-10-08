from os import environ

from flask import Flask

from voice.ext import db


def create_app() -> 'Flask':
    """
    Create application

    :return: flask application object
    """
    app = Flask(__name__)
    app.config.from_object(environ.get('VOICE_CONFIG', 'config.ProductionConfig'))
    db.init_app(app)
    return app
