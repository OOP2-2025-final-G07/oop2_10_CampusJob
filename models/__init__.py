from peewee import SqliteDatabase
from .db import db
from .user import User        # 学籍番号, 性別, 学年
from .job import Job          # 職種, 仕事内容
from .registration import Registration  # user選択, job選択, 時給

# Peewee で作るテーブル一覧
MODELS = [
    User,
    Job,
    Registration,
]

# DB初期化
def initialize_database():
    db.connect()
    db.create_tables(MODELS, safe=True)
    db.close()
