from flask import Blueprint

job_bp = Blueprint('job', __name__)

@job_bp.route('/jobs')
def list():
    return "アルバイト一覧"
