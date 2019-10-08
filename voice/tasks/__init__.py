from flask import Flask
from celery.task import Task

from voice.ext import celery
from voice.tasks import detection


def init_app(app: 'Flask') -> None:
    celery.conf.update(app.config['CELERY'])

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    setattr(celery, 'Task', ContextTask)


@celery.task(name='voice.tasks.phone_detection', bind=True, max_retries=3, default_retry_delay=3 * 60,
             ignore_result=True)
def phone_detection(self: 'Task', entity_id: int) -> None:
    detection.phone_detection(self, entity_id)
