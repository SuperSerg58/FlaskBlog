from webapp.news.models import News
from flask import Blueprint, render_template, current_app
from webapp.weather import weather_by_city

blueprint = Blueprint('news', __name__)


@blueprint.route('/')
def index():
    title = 'Main Page'
    weather = weather_by_city(current_app.config['WEATHER_DEFAULT_CITY'])
    news_list = News.query.order_by(News.published.desc()).all()  # Достает список новостей из БД
    return render_template('news/index.html', title=title, weather=weather, news_list=news_list)
