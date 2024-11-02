from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Repository(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255))
    language = db.Column(db.String(100))
    stargazers_count = db.Column(db.Integer)
    username = db.Column(db.String(100))