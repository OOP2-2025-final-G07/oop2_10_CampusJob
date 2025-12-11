from peewee import Model, CharField
from .db import db

class Job(Model):
    occupation = CharField()      # 職種
    work_detail = CharField()     # 仕事内容

    class Meta:
        database = db
