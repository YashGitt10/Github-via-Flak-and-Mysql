import os
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
import requests
from config import Config 
from models import db, Repository
from services import repo_service

# Flask app initialization
app = Flask(__name__)
app.config.from_object(Config)

# Initialize the database
db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/repos', methods=['GET']) 
def get_repos():
    username = request.args.get('username')
    if not username:
        return render_template('index.html', error="Username is required")

    url = f"https://api.github.com/users/{username}/repos"
    headers = {
        'Authorization': f"token {app.config['GITHUB_TOKEN']}"  # Added space after 'token'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        repos = response.json()
        for repo in repos:
            existing_repo = repo_service.get_repo_by_repo_and_username(repo['name'], username)
            if not existing_repo:
                new_repo = Repository(
                    name=repo['name'],
                    description=repo.get('description'),
                    language=repo.get('language'),
                    stargazers_count=repo.get('stargazers_count'),
                    username=username
                )
                db.session.add(new_repo)
        db.session.commit()
        return render_template('index.html', repos=repos)
    else:
        return render_template('index.html', error="Failed to fetch the repositories")

# Create database tables
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)