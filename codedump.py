@app.route('/quiz/<quiz_link>', methods=["GET", "POST"])
def quiz(quiz_link):
    form = QuizDone()
    if request.method == "POST":

        return redirect(url_for('result'))

    else:
        quiz = Quiz.query.get_or_404(quiz_link)
        quiztext = quiz.quiztitle
        print(quiztext)
        for question in quiz.questions:
            print(question)
        quiz = Quiz.query.filter_by(id=quiz_link).paginate(1, 1, False)
        print(quiz)
        quiz = quiz.items
        print(quiz)
        question = Question.query.filter_by(quiz_id=quiz_link).paginate(1, 2, False)
        print(question)
        q = question.items
        print(q)
        for a in q:
            print(a.answers)
            for b in a.answers:
                print(b.atext)
        return render_template('quiz.html', quiz=quiz, question=question.items, form=form)



@app.route('/quiz/<quiz_link>/<question_link>', methods=["GET", "POST"])
def question(quiz_link, question_link):
        form = QuizDone()
        quiz = Quiz.query.get_or_404(quiz_link)
        question = Question.query.get_or_404(question_link)
        questions = Question.query.filter_by(quiz_id=quiz_link)
        question = Question.query.filter_by(id=question_link)

        user_answer = {}
        session['user_answer'] = user_answer
        user_questions_answered = []
        questions_left = []


        if request.method == "POST":
            for q in questions:
                for answered in user_questions_answered:
                    if q.id == answered['question_id']:
                        questions_left.remove(q.id)

        return redirect(url_for('question', quiz_link=quiz_link, question_link=question_link))

        else:

            return render_template('question.html', quiz=quiz, question=question, form=form)


#working picture saving without resize!
def save_picture(form_picture):
    image = form_picture
    image_filename = secure_filename(image.filename)
    image.save(os.path.join(app.root_path, 'static/images', image_filename))



    return image_filename

# request.method POST-al működik, validate-el nem?
    if form.validate_on_submit():
        print("form validation")
        if form.qpic.data:
            qimage = save_picture(form.qpic.data)
            question = Question(qtext=form.qtext.data, qpic=qimage, quiz_id=quizid)
            db.session.add(question)
            db.session.commit()
            print("got to qpic upload")
        else:
            question = Question(qtext=form.qtext.data, quiz_id=quizid)
            db.session.add(question)
            db.session.commit()
            print("no qpic upload for you")

        q_id = question.id

        alloptions = [[form.atext1.data, form.correct1.data], [form.atext2.data, form.correct2.data], [form.atext3.data, form.correct3.data], [form.atext4.data, form.correct4.data]]
        for b, c in alloptions:
            option = Option(atext=b, correct=c, question_id=q_id)
            db.session.add(option)
            db.session.commit()
            print("for loop works")

        print("it does not get here")

        flash('Question has been added!', 'success')

        # két irányba mehet, ha befejezte a quizt akkor vissza a főoldalra, vagy gyűjtőre. Ha hozzáad kérdést akkor a következő kérdés oldalra.

        return redirect(url_for('addquestion', quizid=quizid, form=form))

    return render_template('addquestion.html', form=form)



### NEW Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=False, nullable=False)
    quizes = db.relationship('Quiz', backref='kviz', lazy=True)

# Ezt újra hozzá kell adni aztán legenerálni az adatbázist!
class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quizname = db.Column(db.String(20), unique=True, nullable=False)
    quiztitle = db.Column(db.String(80), unique=False, nullable=False)
    questions = db.relationship('Question', backref='ques', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    timestamp = db.Column(??????)

# NEW forms

class Register(FlaskForm):

    email = StringField('User Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Register')

class Login(FlaskForm):

    email = StringField('User Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

    submit = SubmitField('Login')
