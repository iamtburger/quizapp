from flask import render_template, url_for, flash, redirect, request, session
from quizapp import app, db
from quizapp.forms import NewQuiz, NewQuestion
from quizapp.models import Quiz, Question, Answer
from werkzeug.utils import secure_filename
import os

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

#do a dynamic url for the quiz questions?
@app.route('/quiz')
def quiz():
    return render_template('quiz.html')

def save_picture(form_picture):
    image = form_picture
    image_filename = secure_filename(image.filename)
    image.save(os.path.join(app.root_path, 'images', image_filename))

    return image_filename

@app.route('/addquestion/', methods=["GET", "POST"])
def addquestion():

    form = NewQuestion()
    #javítani a quiz id részt, melyik legyen a primary key???
    quizname = session['q_id']

    if request.method == "POST":

        qimage = save_picture(form.qpic.data)
        question = Question(qtext=form.qtext.data, qpic=qimage, quiz_id=quizname)
        db.session.add(question)
        db.session.commit()

        q_id = question.id

        allanswers = [[form.apic1.data, form.atext1.data, form.correct1.data], [form.apic2.data, form.atext2.data, form.correct2.data], [form.apic3.data, form.atext3.data, form.correct3.data], [form.apic4.data, form.atext4.data, form.correct4.data]]
        for a, b, c in allanswers:
            aimage = save_picture(a)
            answer = Answer(atext=b, apic=aimage, correct=c, question_id=q_id)
            db.session.add(answer)
            db.session.commit()


        flash('Question has been added!', 'success')

        # két irányba mehet, ha befejezte a quizt akkor vissza a főoldalra, vagy gyűjtőre. Ha hozzáad kérdést akkor a következő kérdés oldalra.

        return redirect(url_for('addquestion', quizname=quizname))

    else:
        return render_template('addquestion.html', form=form)

@app.route('/add-quiz', methods=["GET", "POST"])
def addquiz():
    form = NewQuiz()

    if request.method == "POST":

        quiz = Quiz(quizname=form.quizname.data, quiztitle=form.quiztitle.data)

        db.session.add(quiz)
        db.session.commit()

        session['q_id'] = quiz.id

        # ezt ellenőrizni, hogy működik-e és ezt átadni? akkor viszont javítani kell a következő oldalon a paramétereket!

        flash('The quiz has been created. Now add a question!', 'success')

        return redirect(url_for('addquestion', quizname=session['q_id']))

    else:
        return render_template('add-quiz.html', form=form)
