from os import environ

from flask import Flask


def create_app() -> 'Flask':
    """
    Create application

    :return: flask application object
    """
    app = Flask(__name__)
    app.config.from_object(environ.get('VOICE_CONFIG', 'config.ProductionConfig'))
    return app
