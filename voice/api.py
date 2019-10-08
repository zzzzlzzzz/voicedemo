from datetime import datetime

from flask import Blueprint, current_app, request
from xmlschema import XMLSchemaValidationError

from voice.ext import db
from voice.models import Entity, Service, Phone, Email


bp = Blueprint('api', __name__, url_prefix='/')


datetime_format = '%Y-%m-%d %H:%M:%S'


@bp.route('entity', methods=('POST', ))
def entity():
    data = bp.entity_schema.to_dict(request.data.decode())
    for entity_data in data.values():
        item = Entity(entity_data['Name'])
        for email in entity_data['Email'].split(';'):
            item.emails.append(Email(email))
        for phone in entity_data['Phone'].split(';'):
            item.phones.append(Phone(phone))
        for service_data in entity_data['Services'].values():
            for service in service_data:
                available_from = datetime.strptime(service['Availability']['From'], datetime_format)
                available_to = datetime.strptime(service['Availability']['To'], datetime_format)
                item.services.append(Service(service['Name'], service['@is_main'], available_from, available_to))
        db.session.add(item)
        db.session.commit()
    return '', 201


@bp.errorhandler(XMLSchemaValidationError)
def validation_error(_):
    db.session.rollback()
    return '', 400


@bp.errorhandler(Exception)
def error(_):
    current_app.logger.exception('error')
    db.session.rollback()
    return '', 500
