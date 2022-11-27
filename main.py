from flask import Flask, render_template
from flask_login import LoginManager
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import bd.bd_session
from bd.user import User
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = "SUPER_MEGA_ULTRA_HYPER_SECRET_KEY"


login_manager = LoginManager()
login_manager.init_app(app)
bd.bd_session.global_init('bd/main_bd.sqlite3')


class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = StringField('Пароль', validators=[DataRequired()])


@app.route('/login')
def login_page():
    form = LoginForm()
    bd_sess = bd.bd_session.create_session()
    if form.validate_on_submit():
        login = form.username.data 
        password = form.username.data
        # user = bd_sess.


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


if __name__ == '__main__':
    app.run()