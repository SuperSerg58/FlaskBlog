from flask import Flask, render_template
from webapp.weather import weather_by_city
from webapp.model import db, News


def create_app():
    app = Flask(__name__)  # Создаём приложение фласк
    app.config.from_pyfile('config.py')  # Подключается файл конфигурации
    db.init_app(app)  # Инициализируется База Данных, которая подсасывает константу из конфига

    @app.route('/')
    def index():
        title = 'Main Page'
        weather = weather_by_city(app.config['WEATHER_DEFAULT_CITY'])
        news_list = News.query.order_by(News.published.desc()).all()  # Достает список новостей из БД
        return render_template('index.html', title=title, weather=weather, news_list=news_list)

    return app
