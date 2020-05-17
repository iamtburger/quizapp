from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError


class NewQuiz(FlaskForm):
    quizname = StringField('Quiz Name',
                            validators=[DataRequired(), Length(min=2, max=30)])

    quiztitle = StringField('Quiz Title',
                            validators=[DataRequired(), Length(min=2, max=60)])

    submit = SubmitField('Create Quiz')

    def validate_quiz(self, quizname):
        quiz = Quiz.query.filter_by(quizname=quizname.data).first()
        if quiz:
            raise ValidationError('The Quiz Name is taken. Please choose another one.')

class NewQuestion(FlaskForm):
    qtext = StringField('Question Text',
                        validators[Length(min=5, max=120)]})

    qpic = FileField()

    atext1 = StringField('Answer 1 Text',
                        validators[DataRequired(), Length(min=5, max=120)]})
    apic1 = FileField()
    correct1 = SelectField('Is this answer correct?')

    atext2 = StringField('Answer 2 Text',
                        validators[DataRequired(), Length(min=5, max=120)]})
    apic2 = FileField()
    correct2 = SelectField('Is this answer correct?')


    atext3 = StringField('Answer 3 Text',
                        validators[Length(min=5, max=120)]})
    apic3 = FileField()
    correct3 = SelectField('Is this answer correct?')


    atext4 = StringField('Answer 4 Text',
                        validators[Length(min=5, max=120)]})
    apic4 = FileField()
    correct4 = SelectField('Is this answer correct?')
