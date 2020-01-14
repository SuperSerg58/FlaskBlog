from getpass import getpass  # для ввода пароля из командной строки
import sys

from webapp import create_app
from webapp.db import db
from webapp.user.models import User


app = create_app()

with app.app_context():
    username = input('Enter your name: > ')

    if User.query.filter(User.username == username).count():  # Проверяем есть ли такой пользователь в базе
        print('Пользователь с таким именем уже существует')
        sys.exit(0)

    password = getpass('Введите пароль: ')
    password2 = getpass('Повторите пароль: ')
    if not password == password2:
        print('Пароли не совпадают')
        sys.exit(0)

    new_user = User(username=username, role='admin')
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()
    print('User with id {} added'.format(new_user.id))
