import requests as requests
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from marshmallow import ValidationError
from schemas import IdeaSchema
from models import db, User, Idea


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate = Migrate(app, db)


@app.route('/')
def home():
    return {'status': 'ok'}


@app.route('/users')
def get_users():
    return render_template('users.html', users=User.query.all())


@app.route('/ideas/<int:user_id>', methods=['GET', 'POST'])
def get_idea(user_id):
    if request.method == 'POST':
        activity = requests.get('https://www.boredapi.com/api/activity').json()['activity']
        new_idea = Idea(user_id=user_id, activity=activity)
        db.session.add(new_idea)
        db.session.commit()
    return render_template('ideas.html', ideas=Idea.query.filter_by(user_id=user_id).all(), user=User.query.get(user_id))


@app.route('/create_user', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        name = request.form['name']
        nickname = request.form['nickname']
        new_user = User(name=name, nickname=nickname)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('get_users'))
    else:
        return render_template('create_user.html')


@app.route('/create_idea', methods=['GET', 'POST'])
def create_idea():
    if request.method == 'POST':
        data = request.form
        schema = IdeaSchema()

        try:
            result = schema.load(data)
        except ValidationError as error:
            return render_template('create_idea.html', errors=error.messages, data=data)

        new_idea = Idea(
            activity = result['activity'],
            type = result['type'],
            participants = result['participants'],
            user_id = result['user_id']
    )
        db.session.add(new_idea)
        db.session.commit()
        return redirect(url_for('get_users'))
    else:
        return render_template('create_idea.html', users=User.query.all())


if __name__ == '__main__':
    app.run(debug=True)
