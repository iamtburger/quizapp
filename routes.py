from flask import render_template, url_for, flash, redirect, request, session
from quizapp import app, db
from quizapp.forms import NewQuiz, NewQuestion
from quizapp.models import Quiz, Question, Answer

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

@app.route('/addquestion/', methods=["GET", "POST"])
def addquestion():

    form = NewQuestion()
    #javítani a quiz id részt, melyik legyen a primary key???
    quizname = session['q_id']

    if request.method == "POST":

        question = Question(qtext=form.qtext.data, qpic=form.qpic.data, quiz_id=quizname )
        db.session.add(question)
        db.session.commit()

        q_id = question.id
        answer1 = Answer(atext=form.atext1.data, apic=form.apic1.data, correct=form.correct1.data, question_id=q_id)
        answer2 = Answer(atext=form.atext2.data, apic=form.apic2.data, correct=form.correct2.data, question_id=q_id)
        answer3 = Answer(atext=form.atext3.data, apic=form.apic3.data, correct=form.correct3.data, question_id=q_id)
        answer4 = Answer(atext=form.atext4.data, apic=form.apic4.data, correct=form.correct4.data, question_id=q_id)

        db.session.add(answer1)
        db.session.add(answer2)
        db.session.add(answer3)
        db.session.add(answer4)
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
