from os import environ

from flask import Flask
from xmlschema import XMLSchema

from voice.ext import db
from voice import api


def create_app() -> 'Flask':
    """
    Create application

    :return: flask application object
    """
    app = Flask(__name__)
    app.config.from_object(environ.get('VOICE_CONFIG', 'config.ProductionConfig'))
    db.init_app(app)
    app.register_blueprint(api.bp)
    setattr(api.bp, 'entity_schema', XMLSchema(app.config['ENTITY_XSD']))
    return app
