from peewee import Model, CharField
from .db import db

class Job(Model):
    """
    アルバイト（職種）を表すテーブル用モデルクラス
    Peewee の Model を継承しており、1レコード＝1つの職種データを表す
    """

    # 職種の選択肢
    # (保存される値, 表示用の値) のタプルを並べたもの
    # フォームの<select>や入力制限に利用される
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

    # 職種名を保存するカラム
    # choices を指定することで、OCCUPATION_CHOICES の値のみ登録可能になる
    occupation = CharField(choices=OCCUPATION_CHOICES)

    # 仕事内容を保存するカラム（自由入力）
    work_detail = CharField()

    class Meta:
        # このモデルが使用するデータベースを指定
        # db は db.py で定義された Peewee のデータベース接続
        database = db