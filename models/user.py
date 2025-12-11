from peewee import Model, CharField, IntegerField
from .db import db

class User(Model):
    student_id = CharField()  # 例: "k24084"
    gender = CharField()      # "M" / "F" とか
    grade = IntegerField()    # 1,2,3,4

    class Meta:
        database = db
