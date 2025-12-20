from flask import Blueprint, render_template, request, redirect, url_for
from models import User  # Student ではなく User を使う

user_bp = Blueprint('user', __name__, url_prefix='/users')

@user_bp.route('/')
def list():
    # 修正点：学籍番号（student_id）で昇順ソートを追加しました
    users = User.select().order_by(User.student_id.asc())
    return render_template('user_list.html', title='学生一覧', items=users)

@user_bp.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        User.create(
            name=request.form['name'],
            student_id=request.form['student_id'],
            gender=request.form['gender'],
            grade=request.form['grade']
        )
        return redirect(url_for('user.list'))
    return render_template('user_add.html')

@user_bp.route('/edit/<int:user_id>', methods=['GET', 'POST'])
def edit(user_id):
    user = User.get_or_none(User.id == user_id)
    if not user:
        return redirect(url_for('user.list'))

    if request.method == 'POST':
        user.name = request.form['name']
        user.student_id = request.form['student_id']
        user.gender = request.form['gender']
        user.grade = request.form['grade']
        user.save()
        return redirect(url_for('user.list'))

    return render_template('user_edit.html', user=user)