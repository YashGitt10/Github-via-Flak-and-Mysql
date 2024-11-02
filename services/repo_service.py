# from app import db
from models import Repository

def get_repo_by_repo_and_username(name, username):
    return Repository.query.filter_by(name=name, username=username).first()