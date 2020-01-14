from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_user, logout_user, current_user

from webapp.user.forms import LoginForm
from webapp.user.models import User

blueprint = Blueprint('user', __name__, url_prefix='/users')  # имя_сайта/users/login


@blueprint.route('/login')
def login():
    if current_user.is_authenticated:  # Если пользователь авторизован, то его редиректнет на index
        return redirect(url_for('index'))
    title = 'Авторизация'
    login_form = LoginForm()
    return render_template('login.html', title=title, form=login_form)


@blueprint.route('/process-login', methods=['POST'])
def process_login():
    form = LoginForm()

    if form.validate_on_submit():  # Если с формы пришли данные, например пользователь заполнил поля.
        user = User.query.filter(
            User.username == form.username.data).first()  # Проверяем есть ли такой пользователь
        if user and user.check_password(form.password.data):  # Если пользователь существует в базе
            login_user(user, remember=form.remember_me.data)  # запоминает пользователя если стоит галочка
            flash('{} Вы успешно вошли на сайт'.format(current_user.username))
            return redirect(url_for('index'))

    flash('Неправильные имя или пароль')
    return redirect(url_for('user.login'))


@blueprint.route('/logout')
def logout():
    logout_user()
    flash('Вы успешно разлогинились')
    return redirect(url_for('index'))
