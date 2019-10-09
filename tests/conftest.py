from pytest import fixture
from flask.testing import FlaskClient
from flask_sqlalchemy import SQLAlchemy
from celery import Celery

from voice import create_app
from voice.models import db
from voice.tasks import celery


@fixture(scope='session', autouse=True)
def client() -> 'FlaskClient':
    flask_app = create_app()
    with flask_app.app_context():
        with flask_app.test_client() as c:
            yield c


@fixture(scope='session', autouse=True)
def create_database(client) -> None:
    db.Model.metadata.create_all(bind=db.get_engine())
    yield
    db.Model.metadata.drop_all(bind=db.get_engine())


@fixture(scope='function', autouse=True)
def prepare_database() -> None:
    for _ in reversed(db.Model.metadata.sorted_tables):
        db.session.execute(_.delete())
    db.session.commit()
    yield
    db.session.rollback()


@fixture(scope='session')
def database() -> 'SQLAlchemy':
    yield db


@fixture(scope='session')
def tasks() -> 'Celery':
    yield celery


@fixture(scope='function')
def test_func():
    class TestFunc:
        def __init__(self):
            self.rv = None
            self.called = False
            self.args = None
            self.kwargs = None

        def __call__(self, *args, **kwargs):
            self.called = True
            self.args = args
            self.kwargs = kwargs
            return self.rv
    yield TestFunc()
