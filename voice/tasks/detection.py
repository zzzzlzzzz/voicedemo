import re

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound
from celery.task import Task
from celery.utils.log import get_task_logger

from voice.models import Phone
from voice.ext import db

logger = get_task_logger(__name__)
mobile_phone = re.compile(r'''(\+7|8)\d{10}''')


def phone_detection(self: 'Task', entity_id: int) -> None:
    """Detect type of phone

    :param self: this task
    :param entity_id: id of entity
    """
    try:
        for phone in Phone.query.filter_by(entity_id=entity_id).all():
            phone.is_mobile = bool(mobile_phone.match(phone.phone))
        db.session.commit()
    except NoResultFound:
        pass
    except SQLAlchemyError as e:
        logger.exception('phone_detection')
        self.retry(exc=e)
