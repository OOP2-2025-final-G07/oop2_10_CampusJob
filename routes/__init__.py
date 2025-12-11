from .user import user_bp
from .job import job_bp
from .registration import registration_bp

# Blueprint一覧
blueprints = [
    user_bp,
    job_bp,
    registration_bp
]
