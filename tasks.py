from celery import Celery

from webapp import create_app
from webapp.news.parsers.habr import get_news_snippents, get_news_conntent

flask_app = create_app()
celery_app = Celery('tasks', broker='redis://localhost:6379/0')


@celery_app.task
def habr_snippets():
    with flask_app.app_context():
        get_news_snippents()


@celery_app.task
def habr_content():
    with flask_app.app_context():
        get_news_conntent()
