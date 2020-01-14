from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, current_user, login_required

from webapp.weather import weather_by_city
from webapp.model import db, News

from webapp.user.models import User
from webapp.user.views import blueprint as user_blueprint


def create_app():
    app = Flask(__name__)  # Создаём приложение фласк
    app.config.from_pyfile('config.py')  # Подключается файл конфигурации
    db.init_app(app)  # Инициализируется База Данных, которая подсасывает константу из конфига

    login_manager = LoginManager()  # Создаём экземпляр класса LoginManager
    login_manager.init_app(app)  # Инициализируем его в нашем приложении
    login_manager.login_view = 'user.login'  # Передаем в логин вью название функции, которая этим будет заниматься

    app.register_blueprint(user_blueprint)  # Регистрируем блюпринт Юзеров

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    @app.route('/')
    def index():
        title = 'Main Page'
        weather = weather_by_city(app.config['WEATHER_DEFAULT_CITY'])
        news_list = News.query.order_by(News.published.desc()).all()  # Достает список новостей из БД
        return render_template('index.html', title=title, weather=weather, news_list=news_list)

    @app.route('/admin')
    @login_required
    def admin_index():
        if current_user.is_admin:
            return 'Hello Admin'
        else:
            return 'You are not Admin'

    return app
