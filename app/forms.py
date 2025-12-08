from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, DateField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from flask_wtf.file import FileField, FileAllowed

class RegisterForm(FlaskForm):
    name = StringField('Ονοματεπώνυμο', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Κωδικός', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Επιβεβαίωση Κωδικού', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Εγγραφή')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Κωδικός', validators=[DataRequired()])
    submit = SubmitField('Σύνδεση')

class TaskForm(FlaskForm):
    title = StringField('Τίτλος', validators=[DataRequired()])
    description = TextAreaField('Περιγραφή')
    deadline = DateField('Προθεσμία')
    completed = BooleanField('Ολοκληρώθηκε')
    file = FileField('Αρχείο', validators=[FileAllowed(['pdf', 'doc', 'docx', 'png', 'jpg', 'jpeg'])])  # ✅ Αυτό έλειπε
    submit = SubmitField('Αποθήκευση')