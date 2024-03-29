from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, HiddenField, FieldList, FormField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from wtforms.widgets import TextArea


class CreateQuiz(FlaskForm):
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

class CreateQuestion(FlaskForm):
    qtext = StringField('Question Text',
                        validators=[Length(min=5, max=120)])

    qpic = FileField('Image for question', validators=[FileAllowed(['jpg', 'png'])])

    atext1 = StringField('Correct Answer',
                        validators=[DataRequired(), Length(min=5, max=120)])
    apic1 = FileField('Image for option 1')
    correct1 = BooleanField('Correct Answer!')

    atext2 = StringField('Option 2 Text',
                        validators=[DataRequired(), Length(min=5, max=120)])
    apic2 = FileField('Image for option 2')
    correct2 = BooleanField('Is this option correct?')


    atext3 = StringField('Option 3 Text',
                        validators=[Length(min=5, max=120)])
    apic3 = FileField('Image for option 3')
    correct3 = BooleanField('Is this option correct?')


    atext4 = StringField('Option 4 Text',
                        validators=[Length(min=5, max=120)])
    apic4 = FileField('Image for option 4')
    correct4 = BooleanField('Is this option correct?')

    submit = SubmitField('Add Question')

class UpdateQuestion(FlaskForm):
    qtext = StringField('Question Text',
                        validators=[Length(min=5, max=120)])

    qpic = FileField('Image for question', validators=[FileAllowed(['jpg', 'png'])])

    atext1 = StringField('Correct Answer',
                        validators=[DataRequired(), Length(min=5, max=120)])
    correct1 = BooleanField('Correct Answer!')

    atext2 = StringField('Option 2 Text',
                        validators=[DataRequired(), Length(min=5, max=120)])
    correct2 = BooleanField('Is this option correct?')


    atext3 = StringField('Option 3 Text',
                        validators=[Length(min=5, max=120)])
    correct3 = BooleanField('Is this option correct?')


    atext4 = StringField('Option 4 Text',
                        validators=[Length(min=5, max=120)])
    correct4 = BooleanField('Is this option correct?')

    submit = SubmitField('Update Question')

# class QuizDone(FlaskForm):
#
#     question = HiddenField()
#     option = HiddenField()
#     selected = BooleanField()
#
#     submit = SubmitField('Finish Quiz')

class RegisterForm(FlaskForm):

    email = StringField('User Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Register')

    def check_user(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email is already registered.')

class LoginForm(FlaskForm):

    email = StringField('User Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

    submit = SubmitField('Login')



class TestQuestion(FlaskForm):
    qtext = StringField('Question Text',
                        validators=[Length(min=5, max=120)])

    qpic = FileField('Image for question', validators=[FileAllowed(['jpg', 'png'])])

    atext = StringField('Answer',
                        validators=[DataRequired(), Length(min=5, max=120)])
    correct = BooleanField('Correct Answer!')
    submit = SubmitField('Add Question')

class NewOptionsForm(FlaskForm):
    atext = StringField('Answer', validators=[DataRequired(), Length(min=5, max=120)])
    correct = BooleanField('Correct Answer?')

class NewQuestioForm(FlaskForm):
    qtext = StringField('Question Text', validators=[Length(min=5, max=120)])

    qpic = FileField('Image for question', validators=[FileAllowed(['jpg', 'png'])])
    answers = FieldList(FormField(NewOptionsForm), min_entries=4)
    submit = SubmitField('Add Question')
