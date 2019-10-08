from voice import create_app
from voice.ext import celery


flask_app = create_app()
celery_app = celery
