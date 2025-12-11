from flask import Blueprint, render_template, request, redirect, url_for
from models import Job

# Blueprintの作成
job_bp = Blueprint('job', __name__, url_prefix='/job')


@job_bp.route('/')
def list():
    jobs = Job.select()
    return render_template('Job_list.html', title='アルバイト一覧', items=jobs)


@job_bp.route('/add', methods=['GET', 'POST'])
def add():
    
    # POSTで送られてきたデータは登録
    if request.method == 'POST':
        occupation = request.form['occupation']
        work_detail = request.form['work_detail']
        Job.create(occupation=occupation, work_detail=work_detail)
        return redirect(url_for('job.list'))
    
    return render_template('job_add.html')


@job_bp.route('/edit/<int:job_id>', methods=['GET', 'POST'])
def edit(job_id):
    job = Job.get_or_none(Job.id == job_id)
    if not job:
        return redirect(url_for('job.list'))

    if request.method == 'POST':
        job.occupation = request.form['occupation']
        job.work_detail = request.form['work_detail']
        job.save()
        return redirect(url_for('job.list'))

    return render_template('job_edit.html', job=job)
