from os import environ


class Config:
    SQLALCHEMY_DATABASE_URI = environ.get('VOICE_SQLALCHEMY_DATABASE_URI', '')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = dict(pool_pre_ping=True)


class DevelopmentConfig(Config):
    pass


class TestConfig(Config):
    pass


class ProductionConfig(Config):
    pass
