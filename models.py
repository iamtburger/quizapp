from quizapp import db, login_manager
from flask_login import UserMixin


class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quizname = db.Column(db.String(20), unique=True, nullable=False)
    quiztitle = db.Column(db.String(80), unique=False, nullable=False)
    questions = db.relationship('Question', backref='ques', lazy=True)
    date = db.Column(db.String(120), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    qtext = db.Column(db.String(120), unique=False, nullable=True)
    qpic = db.Column(db.String(20), unique=False, nullable=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    options = db.relationship('Option', backref='opt', lazy=True)

class Option(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    atext = db.Column(db.String(120), unique=False, nullable=True)
    correct = db.Column(db.String(3), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)

class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    range_min = db.Column(db.Integer, nullable=False)
    range_max = db.Column(db.Integer, nullable=False)
    result = db.Column(db.String, unique=False, nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)

@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=False, nullable=False)
    quizes = db.relationship('Quiz', backref='kviz', lazy=True)
