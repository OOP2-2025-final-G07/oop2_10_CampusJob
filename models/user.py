from peewee import Model, CharField
from .db import db

class User(Model):
    name = CharField()
    student_id = CharField()
    gender = CharField()
    grade = CharField()

    class Meta:
        database = db
