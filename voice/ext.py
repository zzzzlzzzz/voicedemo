from flask_sqlalchemy import SQLAlchemy
from celery import Celery


db = SQLAlchemy()
celery = Celery(__name__.split('.', 1)[0])
