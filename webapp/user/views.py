from flask import Blueprint, render_template, flash, redirect, url_for, current_app
from flask_login import login_user, logout_user, current_user
from webapp.weather import weather_by_city

from webapp.db import db
from webapp.user.forms import LoginForm, RegistrationForm
from webapp.user.models import User
from webapp.utils import get_redirect_target

blueprint = Blueprint('user', __name__, url_prefix='/users')  # имя_сайта/users/login


@blueprint.route('/login')
def login():
    if current_user.is_authenticated:  # Если пользователь авторизован, то его редиректнет на index
        return redirect(get_redirect_target())
    title = 'Авторизация'
    login_form = LoginForm()
    weather = weather_by_city(current_app.config['WEATHER_DEFAULT_CITY'])
    return render_template('user/login.html', title=title, form=login_form, weather=weather)


@blueprint.route('/process-login', methods=['POST'])
def process_login():
    form = LoginForm()

    if form.validate_on_submit():  # Если с формы пришли данные, например пользователь заполнил поля.
        user = User.query.filter(
            User.username == form.username.data).first()  # Проверяем есть ли такой пользователь
        if user and user.check_password(form.password.data):  # Если пользователь существует в базе
            login_user(user, remember=form.remember_me.data)  # запоминает пользователя если стоит галочка
            flash('{} Вы успешно вошли на сайт'.format(current_user.username))
            return redirect(get_redirect_target())

    flash('Неправильные имя или пароль')
    return redirect(url_for('user.login'))


@blueprint.route('/logout')
def logout():
    logout_user()
    flash('Вы успешно разлогинились')
    return redirect(url_for('news.index'))


# регистрация пользователей.
@blueprint.route('/register')
def register():
    if current_user.is_authenticated:  # Если пользователь авторизован, то его редиректнет на index
        return redirect(url_for('news.index'))
    title = 'Регистрация'
    form = RegistrationForm()
    weather = weather_by_city(current_app.config['WEATHER_DEFAULT_CITY'])
    return render_template('user/registration.html', page_title=title, form=form, weather=weather)


@blueprint.route('/process-reg', methods=['POST'])
def process_reg():
    form = RegistrationForm()

    if form.validate_on_submit():
        new_user = User(username=form.username.data, email=form.email.data, role='user')
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Вы успешно зарегистрировались на сайте')
        return redirect(url_for('user.login'))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash('Ошибка в поле {} {}'.format(getattr(form, field).label.text, error))
        return redirect(url_for('user.register'))
