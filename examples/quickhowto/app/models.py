import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Enum
from sqlalchemy.orm import relationship
from flask_appbuilder import Model
from marshmallow import Schema, fields, ValidationError, post_load, pre_load

mindate = datetime.date(datetime.MINYEAR, 1, 1)


def validate_name(n):
    if n[0] != 'A':
        raise ValidationError('Name must start with an A')


class ContactGroup(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    def __repr__(self):
        return self.name


class GroupCustomSchema(Schema):
    name = fields.Str(validate=validate_name)

    @post_load
    def process(self, data):
        return ContactGroup(**data)


class ContactGroupSchema(Schema):
    name = fields.Str(required=True)


class Gender(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    def __repr__(self):
        return self.name

import enum


class GenderEnum(enum.Enum):
    male = 'Male'
    female = 'Female'


class Contact(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(150), unique=True, nullable=False)
    address = Column(String(564))
    birthday = Column(Date, nullable=True)
    personal_phone = Column(String(20))
    personal_celphone = Column(String(20))
    contact_group_id = Column(Integer, ForeignKey('contact_group.id'), nullable=False)
    contact_group = relationship("ContactGroup")
    #gender_id = Column(Integer, ForeignKey('gender.id'), nullable=False)
    #gender = relationship("Gender")
    gender = Column(Enum(GenderEnum), nullable=False, info={"enum_class": GenderEnum})

    def __repr__(self):
        return self.name

    def month_year(self):
        date = self.birthday or mindate
        return datetime.datetime(date.year, date.month, 1) or mindate

    def some_function(self):
        return "Hello {}".format(self.name)

    def year(self):
        date = self.birthday or mindate
        return datetime.datetime(date.year, 1, 1)


class ContactSchema(Schema):
    name = fields.Str(required=True)
    address = fields.Str()
    birthday = fields.Date()
    personal_phone = fields.Str()
    personal_celphone = fields.Str()
    contact_group = fields.Nested("ContactGroupSchema", required=True)
    gender = relationship("Gender")
