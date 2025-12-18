from flask import Blueprint, render_template, request, redirect, url_for
from models import Registration, User, Job

registration_bp = Blueprint('registration', __name__, url_prefix='/registrations')

@registration_bp.route('/')
def list():
    registrations = (
        Registration
        .select(Registration, User, Job)
        .join(User)
        .switch(Registration)
        .join(Job)
        .order_by(User.student_id.asc())
    )
    return render_template(
        'registration_list.html',
        title='登録一覧',
        items=registrations
    )

@registration_bp.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        Registration.create(
            user=request.form['user_id'],
            job=request.form['job_id'],
            hourly_wage=request.form['hourly_wage']
        )
        return redirect(url_for('registration.list'))

    users = User.select()
    jobs = Job.select()
    return render_template('registration_add.html', users=users, jobs=jobs)

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
    return render_template('registration_edit.html', registration=registration, users=users, jobs=jobs)

@registration_bp.route('/delete/<int:registration_id>', methods=['POST', 'GET'])
def delete(registration_id):
    registration = Registration.get_or_none(Registration.id == registration_id)
    if registration:
        registration.delete_instance()
    return redirect(url_for('registration.list'))
