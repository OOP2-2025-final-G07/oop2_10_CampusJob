from flask import Blueprint, render_template, request, redirect, url_for
from models import Registration, User, Job

# Blueprintの作成
registration_bp = Blueprint('registration', __name__, url_prefix='/registrations')


@registration_bp.route('/')
def list():
    registrations = Registration.select()
    return render_template('registration_list.html', 
                           title='登録一覧', 
                           items=registrations)


@registration_bp.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        user_id = request.form['user_id']
        job_id = request.form['job_id']
        hourly_wage = request.form['hourly_wage']

        Registration.create(
            user=user_id,
            job=job_id,
            hourly_wage=hourly_wage
        )
        return redirect(url_for('registration.list'))
    
    users = User.select()
    jobs = Job.select()
    return render_template('registration_add.html', 
                           users=users, 
                           jobs=jobs)


@registration_bp.route('/edit/<int:registration_id>', methods=['GET', 'POST'])
def edit(registration_id):
    registration = Registration.get_or_none(Registration.id == registration_id)
    if not registration:
        return redirect(url_for('registration.list'))

    if request.method == 'POST':
        registration.user = request.form['user_id']
        registration.job = request.form['job_id']
        registration.hourly_wage = request.form['hourly_wage']
        registration.save()
        return redirect(url_for('registration.list'))

    users = User.select()
    jobs = Job.select()
    return render_template('registration_edit.html',
                           registration=registration,
                           users=users,
                           jobs=jobs)
