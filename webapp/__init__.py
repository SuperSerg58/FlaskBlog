from flask import Flask, render_template, flash, redirect, url_for
from flask_login import LoginManager, login_user, logout_user
from webapp.weather import weather_by_city
from webapp.model import db, News, User
from webapp.forms import LoginForm


def create_app():
    app = Flask(__name__)  # Создаём приложение фласк
    app.config.from_pyfile('config.py')  # Подключается файл конфигурации
    db.init_app(app)  # Инициализируется База Данных, которая подсасывает константу из конфига

    login_manager = LoginManager()  # Создаём экземпляр класса LoginManager
    login_manager.init_app(app)  # Инициализируем его в нашем приложении
    login_manager.login_view = 'login'  # Передаем в логин вью название функции, которая этим будет заниматься

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    @app.route('/')
    def index():
        title = 'Main Page'
        weather = weather_by_city(app.config['WEATHER_DEFAULT_CITY'])
        news_list = News.query.order_by(News.published.desc()).all()  # Достает список новостей из БД
        return render_template('index.html', title=title, weather=weather, news_list=news_list)

    @app.route('/login')
    def login():
        title = 'Авторизация'
        weather = weather_by_city(app.config['WEATHER_DEFAULT_CITY'])
        login_form = LoginForm()
        return render_template('login.html', title=title, form=login_form, weather=weather)

    @app.route('/process-login', methods=['POST'])
    def process_login():
        form = LoginForm()
        if form.validate_on_submit():  # Если с формы пришли данные, например пользователь не заполнил поля.
            user = User.query.filter(User.username == form.username.data).first()
            if user and user.check_password(
                    form.password.data):  # Если пользователь существует в базе и проверка пароля прошла
                login_user(user)
                flash('Вы успешно вошли на сайт')
                return redirect(url_for('index'))

        flash('Неправильные имя или пароль')
        return redirect(url_for('login'))

    @app.route('/logout')
    def logout():
        logout_user()
        flash('Вы успешно разлогинились')
        return redirect(url_for('index'))

    return app
