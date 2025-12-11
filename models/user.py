from flask import Blueprint, render_template, request, redirect, url_for
from models import Student  # UserではなくStudentをインポート

# Blueprintの作成
user_bp = Blueprint('user', __name__, url_prefix='/users')

@user_bp.route('/')
def list():
    # データ取得
    users = Student.select()
    return render_template('user_list.html', title='学生一覧', items=users)

@user_bp.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        # フォームからデータを受け取る
        name = request.form['name']
        student_id = request.form['student_id']
        gender = request.form['gender']
        grade = request.form['grade']
        
        # データベースに登録
        Student.create(name=name, student_id=student_id, gender=gender, grade=grade)
        return redirect(url_for('user.list'))
    
    return render_template('user_add.html')

@user_bp.route('/edit/<int:user_id>', methods=['GET', 'POST'])
def edit(user_id):
    # 指定されたIDの学生を取得
    user = Student.get_or_none(Student.id == user_id)
    if not user:
        return redirect(url_for('user.list'))

    if request.method == 'POST':
        # データの更新
        user.name = request.form['name']
        user.student_id = request.form['student_id']
        user.gender = request.form['gender']
        user.grade = request.form['grade']
        user.save()
        return redirect(url_for('user.list'))

    return render_template('user_edit.html', user=user)
