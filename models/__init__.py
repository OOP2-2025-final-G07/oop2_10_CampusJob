from .db import db
from .user import User
from .job import Job
from .registration import Registration

MODELS = [
    User,
    Job,
    Registration,
]

def initialize_database():
    db.connect()
    db.create_tables(MODELS, safe=True)
    db.close()
