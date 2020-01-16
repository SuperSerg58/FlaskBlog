from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo  # Проверяет действительно ли пользователь вбил данные.


class LoginForm(FlaskForm):
    username = StringField('Username:', validators=[DataRequired()], render_kw={"class": "form-control"})
    password = PasswordField('Password:', validators=[DataRequired()], render_kw={"class": "form-control"})
    remember_me = BooleanField('Запомнить меня', default=True, render_kw={"class": "form-check-input"})
    submit = SubmitField('Send', render_kw={"class": "btn btn-primary"})


class RegistrationForm(FlaskForm):
    username = StringField('Username:', validators=[DataRequired()], render_kw={"class": "form-control"})
    email = StringField('E-mail:', validators=[DataRequired(), Email()], render_kw={"class": "form-control"})
    password = PasswordField('Password:', validators=[DataRequired()], render_kw={"class": "form-control"})
    password2 = PasswordField('Re-Enter Password:', validators=[DataRequired(), EqualTo('password')],
                              render_kw={"class": "form-control"})
    submit = SubmitField('Register', render_kw={"class": "btn btn-primary"})