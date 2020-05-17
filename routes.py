from flask import render_template, url_for, flash, redirect, request
from quizing import app, db
from quizing.forms import NewQuiz
from quizing.models import Quiz

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

@app.route('/addquestion/<quizname>', methods=["GET", "POST"])
def addquestion(quizname):

    #javítani a quiz id részt, melyik legyen a primary key???

    if request.method == "POST":

        question = NewQuestion(qtext=form.qtext.data, qpic=form.qpic.data, quiz_id=quizname )
        db.session.add(question)

        q_id = question.id
        anwser1 = NewQuestion(atext=form.atext1.data, apic=form.apic1.data, correct=form.correct1.data, question_id=q_id)
        anwser2 = NewQuestion(atext=form.atext2.data, apic=form.apic2.data, correct=form.correct2.data, question_id=q_id)
        anwser3 = NewQuestion(atext=form.atext3.data, apic=form.apic3.data, correct=form.correct3.data, question_id=q_id)
        anwser4 = NewQuestion(atext=form.atext4.data, apic=form.apic4.data, correct=form.correct4.data, question_id=q_id)

        db.session.add(answer1)
        db.session.add(answer2)
        db.session.add(answer3)
        db.session.add(answer4)
        db.session.commit()

        flash('Question has been added!', 'success')

        # két irányba mehet, ha befejezte a quizt akkor vissza a főoldalra, vagy gyűjtőre. Ha hozzáad kérdést akkor a következő kérdés oldalra.

        return redirect(url_for('addquestion', quizname=quizname))

    else:
        return render_template('add-question.html')

@app.route('/add-quiz', methods=["GET", "POST"])
def addquiz():
    form = NewQuiz()

    if request.method == "POST":

        quiz = Quiz(quizname=form.quizname.data, quiztitle=form.quiztitle.data)
        quizname = form.quizname.data

        db.session.add(quiz)
        db.session.commit()

        # ezt ellenőrizni, hogy működik-e és ezt átadni? akkor viszont javítani kell a következő oldalon a paramétereket!
        q_id = quiz.id

        flash('The quiz has been created. Now add a question!', 'success')

        return redirect(url_for('addquestion', quizname=quizname))

    else:
        return render_template('add-quiz.html', form=form)
