from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from wtforms.widgets import TextArea


class NewQuiz(FlaskForm):
    quizname = StringField('Quiz Name',
                            validators=[DataRequired(), Length(min=2, max=30)])

    quiztitle = StringField('Quiz Title',
                            validators=[DataRequired(), Length(min=2, max=60)])

    result1 = TextAreaField('Text to show for lowest 40%',
                        validators=[DataRequired()], widget=TextArea())

    result2 = TextAreaField('Text to show between 41-70%',
                        validators=[DataRequired()], widget=TextArea())

    result3 = TextAreaField('Text to show above 71%',
                        validators=[DataRequired()], widget=TextArea())

    submit = SubmitField('Create Quiz')

    def validate_quiz(self, quizname):
        quiz = Quiz.query.filter_by(quizname=quizname.data).first()
        if quiz:
            raise ValidationError('The Quiz Name is taken. Please choose another one.')

class NewQuestion(FlaskForm):
    qtext = StringField('Question Text',
                        validators=[Length(min=5, max=120)])

    qpic = FileField('Image for question', validators=[FileAllowed(['jpg', 'png'])])

    atext1 = StringField('Answer 1 Text',
                        validators=[DataRequired(), Length(min=5, max=120)])
    apic1 = FileField('Image for answer 1')
    correct1 = BooleanField('Is this answer correct?')

    atext2 = StringField('Answer 2 Text',
                        validators=[DataRequired(), Length(min=5, max=120)])
    apic2 = FileField('Image for answer 2')
    correct2 = BooleanField('Is this answer correct?')


    atext3 = StringField('Answer 3 Text',
                        validators=[Length(min=5, max=120)])
    apic3 = FileField('Image for answer 3')
    correct3 = BooleanField('Is this answer correct?')


    atext4 = StringField('Answer 4 Text',
                        validators=[Length(min=5, max=120)])
    apic4 = FileField('Image for answer 4')
    correct4 = BooleanField('Is this answer correct?')

    submit = SubmitField('Add Question')
