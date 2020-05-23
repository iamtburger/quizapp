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
