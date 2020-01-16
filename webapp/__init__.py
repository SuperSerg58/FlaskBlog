from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from webapp.weather import weather_by_city

from webapp.db import db
from webapp.user.models import User
from webapp.news.models import News

from webapp.user.views import blueprint as user_blueprint
from webapp.admin.views import blueprint as admin_blueprint
from webapp.news.views import blueprint as news_blueprint
from webapp.analizelog.views import blueprint as log_blueprint


def create_app():
    app = Flask(__name__)  # Создаём приложение фласк
    app.config.from_pyfile('config.py')  # Подключается файл конфигурации
    db.init_app(app)  # Инициализируется База Данных, которая подсасывает константу из конфига
    migrate = Migrate(app, db)  # Подключаем работу с миграциями

    login_manager = LoginManager()  # Создаём экземпляр класса LoginManager
    login_manager.init_app(app)  # Инициализируем его в нашем приложении
    login_manager.login_view = 'user.login'  # Передаем в логин вью название функции, которая этим будет заниматься

    app.register_blueprint(user_blueprint)  # Регистрируем блюпринт Юзеров
    app.register_blueprint(admin_blueprint)  # Регистрируем блюпринт Админа
    app.register_blueprint(news_blueprint)  # Регистрируем блюпринт Новостей
    app.register_blueprint(log_blueprint)  # Регистрируем блюпринт анализатора логов

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    return app
