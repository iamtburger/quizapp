from flask import render_template, url_for, flash, redirect, request, session
from quizapp import app, db, bcrypt
from quizapp.forms import NewQuiz, NewQuestion, QuizDone, RegisterForm, LoginForm
from quizapp.models import Quiz, Question, Option, Result, User
from werkzeug.utils import secure_filename
import os

from PIL import Image
from datetime import datetime
from flask_login import login_user
from sqlalchemy import func


@app.route('/')
def index():
    quiz = Quiz.query.all()
    return render_template('index.html', quiz=quiz)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password!')

    return render_template('login.html', form=form)

@app.route('/register', methods=["GET", "POST"])
def register():

    form = RegisterForm()
    if form.validate_on_submit():

        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('The account has been created. You can login now!', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

#do a dynamic url for the quiz questions?
@app.route('/quiz/<quiz_link>')
def quiz(quiz_link):
    quiz = Quiz.query.get_or_404(quiz_link)
    questions = Question.query.filter_by(quiz_id=quiz_link)
    session['left'] = []
    session['answers'] = []
    session['got_it_right'] = []
    for q in questions:
        session['left'].append(q.id)

    question = session['left'][0]

    return render_template('quiz.html', quiz=quiz, question=question)

def checker(question_id, user_answer):
    correct_answers = Option.query.filter_by(question_id=question_id).filter_by(correct=True).all()
    print(correct_answers)
    got_it_right = []
    for correct in correct_answers:
        for answer in user_answer:
            print(type(correct.id))
            print(type(answer))
            if int(answer) == correct.id:
                print(correct.id)
                got_it_right.append(correct.id)
                print("jó válasz")
    print(got_it_right)
    return got_it_right


@app.route('/quiz/<quiz_link>/<question_link>', methods=["GET", "POST"])
def question(quiz_link, question_link):
        form = QuizDone()
        quiz = Quiz.query.get_or_404(quiz_link)
        questions = Question.query.filter_by(quiz_id=quiz_link)
        qall = session['left']
        qleft = qall[0]
        print(f'következő: {qleft}')
        print(qall)
        answers = session['answers']
        right_answers = session['got_it_right']

        options = Option.query.filter_by(question_id=qleft).order_by(func.random()).all()
        question = Question.query.get(qleft)


        if request.method == "POST":

            answer = request.form.getlist('options')
            print(f"válasz id: {answer}")
            answers.append(answer)
            session['answers'] = answers
            print(f"megválaszolva: {answers}")

            result = checker(qleft, answer)
            if result:
                right_answers.append(result)
                session['got_it_right'] = right_answers
                print(f"ezek jók: {right_answers}")


            if len(qall) == 1:

                return redirect(url_for('result', quiz_id=quiz.id))
            else:
                qall.remove(question.id)
                session['left'] = qall
                print(question.id)
                qleft = qall[0]
                print(f"ennyi kérdés van hátra: {qall}")

                return redirect(url_for('question', quiz_link=quiz.id, question_link=qleft))

        else:

            return render_template('question.html', quiz=quiz, question=question, options=options, form=form)

@app.route('/result')
def result():
    quiz_id = request.args.get('quiz_id')
    got_it_right = session['got_it_right']
    correct_answers = Question.query.filter_by(quiz_id=quiz_id).count()
    messages = Result.query.filter_by(quiz_id=quiz_id).all()
    print(f"this is the message: {messages}")
    print(len(got_it_right))
    print(correct_answers)
    result = round((len(got_it_right) / correct_answers) * 100, 2)
    print(result)
    message_to_show = None
    for message in messages:
        if result <= message.range_max and result >= message.range_min:
            message_to_show = message.result
            print(message_to_show)

    return render_template('result.html', result=result, message=message_to_show)

def save_picture(form_picture):
    image = form_picture
    image_filename = secure_filename(image.filename)
    image_path = os.path.join(app.root_path, 'static/images', image_filename)

    output_size = (640, 500)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(image_path)

    return image_filename

@app.route('/addquestion/', methods=["GET", "POST"])
def addquestion():

    form = NewQuestion()
    #javítani a quiz id részt, melyik legyen a primary key???
    quizid = session['q_id']

    if form.validate_on_submit():

        if form.qpic.data:
            qimage = save_picture(form.qpic.data)
            question = Question(qtext=form.qtext.data, qpic=qimage, quiz_id=quizid)
            db.session.add(question)
            db.session.commit()
        else:
            question = Question(qtext=form.qtext.data, quiz_id=quizid)
            db.session.add(question)
            db.session.commit()

        q_id = question.id

        alloptions = [[form.atext1.data, form.correct1.data], [form.atext2.data, form.correct2.data], [form.atext3.data, form.correct3.data], [form.atext4.data, form.correct4.data]]
        for b, c in alloptions:
            option = Option(atext=b, correct=c, question_id=q_id)
            db.session.add(option)
            db.session.commit()


        flash('Question has been added!', 'success')

        # két irányba mehet, ha befejezte a quizt akkor vissza a főoldalra, vagy gyűjtőre. Ha hozzáad kérdést akkor a következő kérdés oldalra.

        return redirect(url_for('addquestion', quizid=quizid))

    return render_template('addquestion.html', form=form)

@app.route('/add-quiz', methods=["GET", "POST"])
def addquiz():
    form = NewQuiz()

    if form.validate_on_submit():

        quiz = Quiz(quizname=form.quizname.data, quiztitle=form.quiztitle.data, date=datetime.today(), user_id='1')

        db.session.add(quiz)
        db.session.commit()

        session['q_id'] = quiz.id

        ranges = [[0, 40, form.result1.data], [41, 70, form.result2.data], [71, 100, form.result3.data]]
        for a, b, c in ranges:
            result = Result(range_min=a, range_max=b, result=c, quiz_id=quiz.id)
            db.session.add(result)
            db.session.commit()

        # ezt ellenőrizni, hogy működik-e és ezt átadni? akkor viszont javítani kell a következő oldalon a paramétereket!

        flash('The quiz has been created. Now add a question!', 'success')

        return redirect(url_for('addquestion', quizid=session['q_id']))

    return render_template('add-quiz.html', form=form)
