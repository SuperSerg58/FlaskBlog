from celery import Celery
from celery.schedules import crontab
from webapp import create_app
from webapp.news.parsers.habr import get_news_snippents, get_news_conntent

flask_app = create_app()
celery_app = Celery('tasks', broker='redis://127.0.0.1:6379/0')


@celery_app.task
def habr_snippets():
    with flask_app.app_context():
        get_news_snippents()


@celery_app.task
def habr_content():
    with flask_app.app_context():
        get_news_conntent()


@celery_app.on_after_configure.connect
def setup_pereodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(minute='*/1'), habr_snippets.s())
    sender.add_periodic_task(crontab(minute='*/1'), habr_content.s())
