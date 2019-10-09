from datetime import datetime

from flask.testing import FlaskClient
from flask_sqlalchemy import SQLAlchemy
from celery import Celery


from voice.models import Entity


valid_data = '''<?xml version="1.0"?>
<Body>
  <Entity>
      <Name>Name</Name>
      <Phone>+77772347122;89999999999</Phone>
      <Email>login@domain.com;login2@domain.com</Email>
      <Services>
        <Service is_main = "true">
            <Name>Service</Name>
            <Availability>
                <From>2019-01-01 00:00:00</From>
                <To>2019-12-01 23:59:59</To>
            </Availability>
        </Service>
        <Service is_main = "false">
            <Name>Service 2</Name>
            <Availability>
                <From>2019-02-01 00:00:00</From>
                <To>2019-11-01 23:59:59</To>
            </Availability>
        </Service>
      </Services>
  </Entity>
</Body>
'''


invalid_data = '''<?xml version="1.0"?>
<Body>
  <Entity>
      <Jame>Name</Name>
      <Phone>+77772347122;89999999999</Phone>
      <Email>login@domain.com;login2@domain.com</Email>
      <Services>
        <Service is_main = "true">
            <Name>Service</Name>
            <Availability>
                <From>2019-01-01 00:00:00</From>
                <To>2019-12-01 23:59:59</To>
            </Availability>
        </Service>
        <Service is_main = "false">
            <Name>Service 2</Name>
            <Availability>
                <From>2019-02-01 00:00:00</From>
                <To>2019-11-01 23:59:59</To>
            </Availability>
        </Service>
      </Services>
  </Entity>
</Body>
'''


invalid_data_2 = '''<?xml version="1.0"?>
<Body>
  <Entity>
      <Krex>Name</Krex>
      <Phone>+77772347122;89999999999</Phone>
      <Email>login@domain.com;login2@domain.com</Email>
      <Services>
        <Service is_main = "true">
            <Name>Service</Name>
            <Availability>
                <From>2019-01-01 00:00:00</From>
                <To>2019-12-01 23:59:59</To>
            </Availability>
        </Service>
        <Service is_main = "false">
            <Name>Service 2</Name>
            <Availability>
                <From>2019-02-01 00:00:00</From>
                <To>2019-11-01 23:59:59</To>
            </Availability>
        </Service>
      </Services>
  </Entity>
</Body>
'''


def test_api_valid(monkeypatch, test_func, client: 'FlaskClient', tasks: 'Celery', database: 'SQLAlchemy') -> None:
    monkeypatch.setattr(tasks, 'send_task', test_func)
    rv = client.post('/entity', headers={'Content-type': 'text/xml'}, data=valid_data)
    assert rv.status_code == 201
    assert test_func.called
    entity = database.session.query(Entity).get(test_func.args[1][0])
    assert entity
    assert entity.name == 'Name'
    for email in entity.emails:
        if email.email not in ['login@domain.com', 'login2@domain.com']:
            assert False
    for phone in entity.phones:
        if phone.phone not in ['+77772347122', '89999999999']:
            assert False
    for service in entity.services:
        if service.name == 'Service':
            assert service.is_main
            assert service.available_from == datetime(2019, 1, 1, 0, 0, 0)
            assert service.available_to == datetime(2019, 12, 1, 23, 59, 59)
        elif service.name == 'Service 2':
            assert not service.is_main
            assert service.available_from == datetime(2019, 2, 1, 0, 0, 0)
            assert service.available_to == datetime(2019, 11, 1, 23, 59, 59)
        else:
            assert False


def test_api_invalid(monkeypatch, test_func, client: 'FlaskClient', tasks: 'Celery') -> None:
    monkeypatch.setattr(tasks, 'send_task', test_func)
    rv = client.post('/entity', headers={'Content-type': 'text/xml'}, data=invalid_data)
    assert rv.status_code == 400
    assert not test_func.called


def test_api_invalid_2(monkeypatch, test_func, client: 'FlaskClient', tasks: 'Celery') -> None:
    monkeypatch.setattr(tasks, 'send_task', test_func)
    rv = client.post('/entity', headers={'Content-type': 'text/xml'}, data=invalid_data_2)
    assert rv.status_code == 400
    assert not test_func.called
