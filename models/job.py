from peewee import Model, CharField
from .db import db

class Job(Model):
    # 職種の選択肢
    OCCUPATION_CHOICES = (
        ('飲食', '飲食'),
        ('事務', '事務'),
        ('小売', '小売'),
        ('作業', '作業'),
        ('教育', '教育'),
        ('マスコミ', 'マスコミ'),
        ('エンタメ', 'エンタメ'),
        ('在宅', '在宅'),
        ('その他', 'その他')
    )

    occupation = CharField(choices=OCCUPATION_CHOICES) # 職種
    work_detail = CharField() # 仕事内容

    class Meta:
        database = db
