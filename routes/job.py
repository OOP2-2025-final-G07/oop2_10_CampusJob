# Flask関連のインポート
# Blueprint: 機能ごとにルーティングを分割するための仕組み
# render_template: HTMLテンプレートを表示する
# request: フォームから送信されたデータを取得する
# redirect, url_for: 処理後に別のページへ移動する
from flask import Blueprint, render_template, request, redirect, url_for

# モデルのインポート
# Job: アルバイト（職種）マスタ
# Registration: 登録情報（Jobが使われているか確認するために使用）
from models import Job, Registration

# peewee関連
# fn: SQLの集計関数（COUNTなど）を使うため
# JOIN: JOINの種類（LEFT OUTER JOINなど）を指定するため
from peewee import fn, JOIN

# Blueprintの作成
# 'job' はBlueprint名、url_prefix='/job' によりURLは /job/... になる
job_bp = Blueprint('job', __name__, url_prefix='/job')

# -----------------------------
# アルバイト一覧表示
# -----------------------------
@job_bp.route('/')
def list():
    # Jobごとに「何件のRegistrationで使われているか」を集計するクエリ
    jobs = (
        Job
        .select(
            Job,  # Jobテーブルの全カラム
            fn.COUNT(Registration.id).alias('usage_count')  # 使用回数をusage_countとして取得
        )
        .join(Registration, JOIN.LEFT_OUTER)  # RegistrationがなくてもJobを表示するためLEFT OUTER JOIN
        .group_by(Job)  # Job単位で集計
    )

    # job_list.html にデータを渡して表示
    return render_template(
        'job_list.html',
        title='アルバイト一覧',
        items=jobs
    )

# -----------------------------
# アルバイト追加
# -----------------------------
@job_bp.route('/add', methods=['GET', 'POST'])
def add():
    # フォーム送信（POST）の場合
    if request.method == 'POST':
        # フォームの入力値を使って新しいJobを作成
        Job.create(
            occupation=request.form['occupation'],
            work_detail=request.form['work_detail']
        )
        # 追加後は一覧画面へ戻る
        return redirect(url_for('job.list'))

    # GETの場合は追加画面を表示
    return render_template('job_add.html')

# -----------------------------
# アルバイト編集
# -----------------------------
@job_bp.route('/edit/<int:job_id>', methods=['GET', 'POST'])
def edit(job_id):
    # 指定されたIDのJobを取得（存在しない場合はNone）
    job = Job.get_or_none(Job.id == job_id)
    if not job:
        # データが存在しない場合は一覧へ戻す
        return redirect(url_for('job.list'))

    # フォーム送信（POST）の場合
    if request.method == 'POST':
        # 入力された内容で更新
        job.occupation = request.form['occupation']
        job.work_detail = request.form['work_detail']
        job.save()
        # 更新後は一覧画面へ戻る
        return redirect(url_for('job.list'))

    # GETの場合は編集画面を表示（既存データを渡す）
    return render_template('job_edit.html', job=job)

# -----------------------------
# アルバイト削除
# -----------------------------
@job_bp.route('/delete/<int:job_id>')
def delete(job_id):
    # 指定されたIDのJobを取得
    job = Job.get_or_none(Job.id == job_id)
    if not job:
        # 存在しない場合は一覧へ戻す
        return redirect(url_for('job.list'))

    # このJobがRegistrationで何件使われているかを確認
    used_count = Registration.select().where(
        Registration.job == job
    ).count()

    # 使用されていない場合のみ削除
    if used_count == 0:
        job.delete_instance()
    # else:
    # 使用中の場合は削除しない（安全対策）

    # 処理後は一覧画面へ戻る
    return redirect(url_for('job.list'))