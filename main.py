from flask import Flask, render_template
import flask
from flask_login import LoginManager, login_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField
from wtforms.validators import DataRequired
import bd.bd_session
from bd.user import User
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = "SUPER_MEGA_ULTRA_HYPER_SECRET_KEY"


login_manager = LoginManager()
login_manager.init_app(app)
bd.bd_session.global_init('bd/main_bd.sqlite3')


class NewUserForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Создать')


class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


def search_user(username):
    db_sess = bd.bd_session.create_session()
    user = db_sess.query(User).filter(User.username == username).first()
    return user


@app.route('/new_user', methods=['GET', 'POST'])
def new_user():
    form = NewUserForm()
    db_sess = bd.bd_session.create_session()
    if form.validate_on_submit():
        is_exist = db_sess.query(User).filter(User.username == form.username.data).first()
        if is_exist:
            return render_template('error.html', title='Ошибка', error='Пользователь с таким логином уже существует')
        user = User()
        user.first_name = form.name.data
        user.second_name = form.surname.data
        user.username = form.username.data
        user.password = form.password.data
        db_sess.add(user)
        db_sess.commit()
        return flask.redirect('/login')

    return render_template('new_user.html', title='Новый аккаунт', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = search_user(username)
        if not user:
            return render_template('login.html', title='Авторизация', form=form, alert='Пользователь не найден!')
        elif user.password != password:
            return render_template('login.html', title='Авторизация', form=form, alert='Неверный пароль!')
        login_user(user, remember=form.remember_me.data)
        return flask.redirect('/')

    if not current_user.is_authenticated:
        return render_template('login.html', title='Авторизация', form=form, alert=None)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='30 лет СурГУ')


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


if __name__ == '__main__':
    app.run()