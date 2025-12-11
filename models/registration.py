from peewee import Model, ForeignKeyField, IntegerField
from .db import db
from .user import User
from .job import Job

class Registration(Model):
    user = ForeignKeyField(User, backref='registrations')
    job = ForeignKeyField(Job, backref='registrations')
    hourly_wage = IntegerField()

    class Meta:
        database = db
