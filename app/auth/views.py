# coding=utf-8
from flask import render_template, flash, redirect, url_for
from flask import request

from . import auth
from .forms import LoginForm, RegistrationForm
from ..models import User
from .. import db
from flask_login import login_user, logout_user, current_user


@auth.route('/')
def home():
    return render_template('home.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user  = User(username = form.username.data,
                     password = form.password.data,
                     email = form.email.data,
                     role_id = 2
                     )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth.login'))
    return render_template('register.html',title = u'注册', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None:
            print '登陆成功'
            login_user(user)
            return redirect(request.args.get('next') or url_for('main.index'))
        else:
            flash('账号或密码错误')
    return render_template('login.html',title = u'登陆', form=form)


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))




