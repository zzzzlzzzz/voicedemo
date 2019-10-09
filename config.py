from os import environ


class Config:
    SQLALCHEMY_DATABASE_URI = environ.get('VOICE_SQLALCHEMY_DATABASE_URI', '')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = dict(pool_pre_ping=True)
    ENTITY_XSD = environ.get('VOICE_ENTITY_XSD', '')
    CELERY = dict(
        broker_url=environ.get('VOICE_CELERY_BROKER_URI', ''),
        worker_max_memory_per_child=256 * 1024,
        task_default_queue='default',
        task_routes={
            'voice.tasks.phone_detection': {
                'queue': 'detection',
            },
        },
    )


class DevelopmentConfig(Config):
    pass


class TestConfig(Config):
    TESTING = True
    CELERY = {
        **Config.CELERY,
        'task_always_eager': True,
        'task_eager_propagates': True,
    }


class ProductionConfig(Config):
    pass
