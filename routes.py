from flask import render_template, url_for, flash, redirect, request, session, abort
from quizapp import app, db, bcrypt
from quizapp.forms import CreateQuiz, CreateQuestion, RegisterForm, LoginForm, UpdateQuestion
from quizapp.models import Quiz, Question, Option, Result, User
from werkzeug.utils import secure_filename
import os

from PIL import Image
from datetime import datetime
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy import func

# Main page, showing the list of quizes that were created by the user.
@app.route('/')
@login_required
def index():
    quiz = Quiz.query.all()
    return render_template('index.html', quiz=quiz)

# Login route. logging in with email and password.
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password!')

    return render_template('login.html', form=form)

# Logout route
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

# Register route
@app.route('/register', methods=["GET", "POST"])
def register():

    # Check if the user is logged in and if true return to main page.
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    # If the user is not logged, they can do the registration. Password is hashed with bcrypt. Registration is with email address.
    if form.validate_on_submit():

        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('The account has been created. You can login now!', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

# Quiz route. This is the first page of the quiz. Basically this is the start button on the beginning of a quiz.
@app.route('/quiz/<quiz_link>')
def quiz(quiz_link):
    quiz = Quiz.query.get_or_404(quiz_link)
    questions = Question.query.filter_by(quiz_id=quiz_link)
    session['questions_left'] = []
    session['answers'] = []
    session['got_it_right'] = []
    session['correct_counter'] = 0
    for q in questions:
        session['questions_left'].append(q.id)

    question = session['questions_left'][0]

    return render_template('quiz.html', quiz=quiz, question=question)

# Function to check if the answer by the user was correct.
def checker(question_id, user_answer):
    correct_answers = Option.query.filter_by(question_id=question_id).filter_by(correct=True).all()
    question = Question.query.get(question_id)
    print(correct_answers)
    got_it_right = []
    for correct in correct_answers:
        for answer in user_answer:
            print(type(correct.id))
            print(answer)
            # If the answer is right
            if int(answer) == correct.id:
                print(correct.id)
                got_it_right.extend([question.qtext, correct.atext])
                print("jó válasz")
            # If the answer is wrong
            else:
                user_answered = Option.query.get(answer)
                got_it_right.extend([question.qtext, correct.atext, user_answered.atext])
    print(got_it_right)
    return got_it_right

# Question shown to the user.
@app.route('/quiz/<quiz_link>/<question_link>', methods=["GET", "POST"])
def question(quiz_link, question_link):
        quiz = Quiz.query.get_or_404(quiz_link)
        questions = Question.query.filter_by(quiz_id=quiz_link)
        # The questions of the quiz that are still to be answered.
        remaining_questions = session['questions_left']
        # The next question in the quiz.
        next_question = remaining_questions[0]
        print(f'következő: {next_question}')
        print(remaining_questions)
        # Saving the answers of the user
        answers = session['answers']
        # Correct answers by the user
        right_answers = session['got_it_right']

        options = Option.query.filter_by(question_id=next_question).order_by(func.random()).all()
        question = Question.query.get(next_question)


        if request.method == "POST":

            answer = request.form.getlist('options')
            print(f"válasz id: {answer}")
            answers.append(answer)
            session['answers'] = answers
            print(f"megválaszolva: {answers}")

            result = checker(next_question, answer)
            right_answers.append(result)
            session['got_it_right'] = right_answers
            if len(result) == 2:
                session['correct_counter'] += 1


            # If there is only one question left after answering it the next page will be the result page.
            if len(remaining_questions) == 1:

                return redirect(url_for('result', quiz_id=quiz.id))
            # If there are more than one questions, it shows the next question to the user.
            else:
                remaining_questions.remove(question.id)
                session['questions_left'] = remaining_questions
                print(question.id)
                next_question = remaining_questions[0]
                print(f"ennyi kérdés van hátra: {remaining_questions}")

                return redirect(url_for('question', quiz_link=quiz.id, question_link=next_question))

        else:

            return render_template('question.html', quiz=quiz, question=question, options=options)

# Showing the result of the quiz to the user. What is their overall score.
@app.route('/result')
def result():
    quiz_id = request.args.get('quiz_id')
    got_it_right = session['got_it_right']
    correct_answers = Question.query.filter_by(quiz_id=quiz_id).count()
    messages = Result.query.filter_by(quiz_id=quiz_id).all()
    print(f"this is the message: {messages}")
    print(f"Got these right: {got_it_right}")
    print(correct_answers)
    result = round((session['correct_counter'] / correct_answers) * 100, 2)
    print(result)
    message_to_show = None
    for message in messages:
        if result <= message.range_max and result >= message.range_min:
            message_to_show = message.result
            print(message_to_show)

    return render_template('result.html', result=result, message=message_to_show, got_it_right=got_it_right)

# Function for saving a picture.
def save_picture(form_picture):
    image = form_picture
    image_filename = secure_filename(image.filename)
    image_path = os.path.join(app.root_path, 'static/images', image_filename)

    output_size = (640, 500)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(image_path)

    return image_filename

# Adding a question to a quiz.
@app.route('/addquestion/', methods=["GET", "POST"])
def addquestion():

    form = CreateQuestion()
    #javítani a quiz id részt, melyik legyen a primary key???
    quizid = request.args.get('quizid')

    if form.validate_on_submit():

        # If the quiz has a picture it will save it to the databse.
        if form.qpic.data:
            qimage = save_picture(form.qpic.data)
            question = Question(qtext=form.qtext.data, qpic=qimage, quiz_id=quizid)
            db.session.add(question)
            db.session.commit()
        # If there is no picture it will only save the text.
        else:
            question = Question(qtext=form.qtext.data, quiz_id=quizid)
            db.session.add(question)
            db.session.commit()

        q_id = question.id

        # Saving the options to the database
        alloptions = [[form.atext1.data, form.correct1.data], [form.atext2.data, form.correct2.data], [form.atext3.data, form.correct3.data], [form.atext4.data, form.correct4.data]]
        for b, c in alloptions:
            option = Option(atext=b, correct=c, question_id=q_id)
            db.session.add(option)
            db.session.commit()

        flash('Question has been added!', 'success')

        return redirect(url_for('addquestion', quizid=quizid))

    return render_template('addquestion.html', form=form)

# Creating a quiz.
@app.route('/add-quiz', methods=["GET", "POST"])
def addquiz():
    form = CreateQuiz()

    if form.validate_on_submit():

        quiz = Quiz(quizname=form.quizname.data, quiztitle=form.quiztitle.data, date=datetime.today(), user_id='1')

        db.session.add(quiz)
        db.session.commit()

        quizid = quiz.id

        # The ranges for the answers are pre-defined at the moment.
        ranges = [[0, 40, form.result1.data], [41, 70, form.result2.data], [71, 100, form.result3.data]]
        for a, b, c in ranges:
            result = Result(range_min=a, range_max=b, result=c, quiz_id=quiz.id)
            db.session.add(result)
            db.session.commit()

        # ezt ellenőrizni, hogy működik-e és ezt átadni? akkor viszont javítani kell a következő oldalon a paramétereket!

        flash('The quiz has been created. Now add a question!', 'success')

        return redirect(url_for('addquestion', quizid=quizid))

    return render_template('add-quiz.html', form=form)

# List of questions in a quiz.
@app.route('/<quiz_link>/question-list')
def questionlist(quiz_link):

    question_list = Question.query.filter_by(quiz_id=quiz_link).all()
    return render_template('question-list.html', question_list=question_list)

@app.route('/<quiz_link>/update/<question_link>', methods=['GET', 'POST'])
def update(quiz_link, question_link):
    question = Question.query.filter_by(quiz_id=quiz_link).first()
    quiz = Quiz.query.filter_by(id=quiz_link).first()
    option_list = Option.query.filter_by(question_id=question_link).all()
    if current_user.id != quiz.user_id:

        abort(403)

    form = UpdateQuestion()
    if form.validate_on_submit():

        question.qtext = form.qtext.data
        option_list[0].atext = form.atext1.data
        option_list[1].atext = form.atext2.data
        option_list[2].atext = form.atext3.data
        option_list[3].atext = form.atext4.data
        db.session.commit()
        flash('The Question has been updated', 'success')
        return redirect(url_for('questionlist', quiz_link=quiz_link))

    elif request.method == 'GET':
        form.qtext.data = question.qtext
        form.atext1.data = option_list[0].atext
        form.atext2.data = option_list[1].atext
        form.atext3.data = option_list[2].atext
        form.atext4.data = option_list[3].atext
    return render_template('update.html', option_list=option_list, question=question, form=form)

# Deleting a quiz.
@app.route('/<quiz_link>/delete-quiz', methods=['POST'])
def deletequiz(quiz_link):
    quiz = Quiz.query.filter_by(id=quiz_link).first()
    questions = Question.query.filter_by(quiz_id=quiz_link).all()


    if current_user.id != quiz.user_id:
        abort(403)

    for question in questions:
        options = Option.query.filter_by(question_id=question.id).all()
        for option in options:
            db.session.delete(option)
        db.session.delete(question)
    db.session.delete(quiz)
    db.session.commit()
    return redirect(url_for('index'))

# Deleting a question.
@app.route('/<quiz_link>/delete-question/<question_link>', methods=['POST'])
def deletequestion(quiz_link, question_link):
    quiz = Quiz.query.filter_by(id=quiz_link).first()
    question = Question.query.get(question_link)

    if current_user.id != quiz.user_id:
        abort(403)


    options = Option.query.filter_by(question_id=question.id).all()
    for option in options:
        db.session.delete(option)
    db.session.delete(question)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/frame')
def frame():
    return render_template('embed.html')

# Error handling
@app.errorhandler(404)
def error_404(e):
    return render_template('404.html'), 404

@app.errorhandler(403)
def error_403(e):
    return render_template('403.html'), 403

@app.errorhandler(500)
def error_500(e):
    return render_template('500.html'), 500

# @app.route('/naq/', methods=["GET", "POST"])
# def naq():
#
#     form = TestQuestion()
#     #javítani a quiz id részt, melyik legyen a primary key???
#     quizid = request.args.get('quizid')
#
#
#     if form.validate_on_submit():
#         pass
#         # # If the quiz has a picture it will save it to the databse.
#         # if form.qpic.data:
#         #     qimage = save_picture(form.qpic.data)
#         #     question = Question(qtext=form.qtext.data, qpic=qimage, quiz_id=quizid)
#         #     db.session.add(question)
#         #     db.session.commit()
#         # # If there is no picture it will only save the text.
#         # else:
#         #     question = Question(qtext=form.qtext.data, quiz_id=quizid)
#         #     db.session.add(question)
#         #     db.session.commit()
#         #
#         # q_id = question.id
#         #
#         # # Saving the options to the database
#         # alloptions = [[form.atext1.data, form.correct1.data], [form.atext2.data, form.correct2.data], [form.atext3.data, form.correct3.data], [form.atext4.data, form.correct4.data]]
#         # for b, c in alloptions:
#         #     option = Option(atext=b, correct=c, question_id=q_id)
#         #     db.session.add(option)
#         #     db.session.commit()
#         #
#         # flash('Question has been added!', 'success')
#         #
#         # return redirect(url_for('addquestion', quizid=quizid))
#
#     return render_template('naq.html', form=form)
