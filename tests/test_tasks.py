from pytest import mark
from flask_sqlalchemy import SQLAlchemy


from voice.models import Entity, Phone
from voice.tasks import phone_detection


@mark.parametrize("phone_number,is_mobile", [('+71234567890', True),
                                             ('81234567890', True),
                                             ('886454123', False), ])
def test_phone_detection(monkeypatch, test_func, database: 'SQLAlchemy', phone_number: str, is_mobile: bool) -> None:
    entity = Entity('Test')
    phone1 = Phone(phone_number)
    phone2 = Phone(phone_number)
    entity.phones.append(phone1)
    entity.phones.append(phone2)
    database.session.add(entity)
    database.session.commit()
    monkeypatch.setattr(phone_detection, 'retry', test_func)
    phone_detection.apply_async((entity.entity_id, ))
    database.session.expire_all()
    assert not test_func.called
    assert phone1.is_mobile == is_mobile and phone2.is_mobile == is_mobile
