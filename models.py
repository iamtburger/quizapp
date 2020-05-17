from quizing import db

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quizname = db.Column(db.String(20), unique=True, nullable=False)
    quiztitle = db.Column(db.String(80), unique=False, nullable=False)
    questions = db.relationship('Question', backref='ques', lazy=True)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    qtext = db.Column(db.String(120), unique=False, nullable=True)
    qpic = db.Column(db.String(20), unique=False, nullable=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    answers = db.relationship('Answer', backref='answ', lazy=True)

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    atext = db.Column(db.String(120), unique=False, nullable=True)
    apic = db.Column(db.String(20), unique=False, nullable=True)
    correct = db.Column(db.String(3), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)