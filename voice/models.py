from datetime import datetime

from voice.ext import db


class Email(db.Model):
    __tablename__ = 'email'

    email_id = db.Column(db.Integer, primary_key=True)
    entity_id = db.Column(db.Integer, db.ForeignKey('entity.entity_id', ondelete='CASCADE'), nullable=False)
    entity = db.relationship('Entity', back_populates='emails')
    email = db.Column(db.String(256), nullable=False)

    def __init__(self, email: str):
        self.email = email


class Phone(db.Model):
    __tablename__ = 'phone'

    phone_id = db.Column(db.Integer, primary_key=True)
    entity_id = db.Column(db.Integer, db.ForeignKey('entity.entity_id', ondelete='CASCADE'), nullable=False)
    entity = db.relationship('Entity', back_populates='phones')
    phone = db.Column(db.String(16), nullable=False)
    is_mobile = db.Column(db.Boolean)

    def __init__(self, phone: str):
        self.phone = phone


class Service(db.Model):
    __tablename__ = 'service'

    service_id = db.Column(db.Integer, primary_key=True)
    entity_id = db.Column(db.Integer, db.ForeignKey('entity.entity_id', ondelete='CASCADE'), nullable=False)
    entity = db.relationship('Entity', back_populates='services')
    name = db.Column(db.String(128), nullable=False)
    is_main = db.Column(db.Boolean, nullable=False)
    available_from = db.Column(db.DateTime, nullable=False)
    available_to = db.Column(db.DateTime, nullable=False)

    def __init__(self, name: str, is_main: bool, available_from: 'datetime', available_to: 'datetime'):
        self.name = name
        self.is_main = is_main
        self.available_from = available_from
        self.available_to = available_to


class Entity(db.Model):
    __tablename__ = 'entity'

    entity_id = db.Column(db.Integer, primary_key=True)
    emails = db.relationship('Email', back_populates='entity', cascade='all, delete-orphan', passive_deletes=True)
    phones = db.relationship('Phone', back_populates='entity', cascade='all, delete-orphan', passive_deletes=True)
    services = db.relationship('Service', back_populates='entity', cascade='all, delete-orphan', passive_deletes=True)
    name = db.Column(db.String(128))

    def __init__(self, name: str):
        self.name = name
