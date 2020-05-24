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
