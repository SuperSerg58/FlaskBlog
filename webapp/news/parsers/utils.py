import requests

from webapp.db import db
from webapp.news.models import News


def get_html(url):
    headers = {
        'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
    }
    try:
        result = requests.get(url, headers=headers)
        result.raise_for_status()
        return result.text
    except(requests.RequestException, ValueError):
        print('Network error')
        return False


def save_news(title, url, published):
    news_exists = News.query.filter(News.url == url).count()  # Считает сколько одинаковых URL в базе
    print(news_exists)
    if not news_exists:  # URL согласно модели News должен быть уникальным. Если таких URL в базе нет, то записываем
        # данные
        news_news = News(title=title, url=url, published=published)
        db.session.add(news_news)
        db.session.commit()
