# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 08:49:58 2017

@author: rbomblies
"""
from flask import render_template, redirect, url_for, request, g, session
from flask_login import login_user, logout_user, current_user, login_required
from datetime import datetime
from simplepam import authenticate

from app import app, db, lm
from .forms import LogForm, LoginForm
from .models import User, Worksession
from .plotting import plot_worksessions

@app.route('/')
@app.route('/index')
@login_required
def index():
    def format_time(time):
        if isinstance(time, datetime):
            return '{}:{}'.format(time.hour, time.minute)
        else:
            return ''
    user = g.user
    #user = {'nickname': 'Rainberto I.'}  # fake user
    worksessions = user.worksessions.all()
    worksessions = worksessions[-10:]
    #for sess in worksessions:
    #    sess.check_in = format_time(sess.check_in)
    #    sess.check_out = format_time(sess.check_out)


    plot = plot_worksessions(worksessions)

    return render_template('index.html',
                           title='Home',
                           plot = plot,
                           user=user,
                           sessions=worksessions)


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_request
def before_request():
    g.user = current_user

@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            remember_me = form.remember_me.data

            user = User.query.filter_by(username=username).first()
            if authenticate(str(username), str(password)):
                login_user(user, remember = remember_me)
                return redirect(url_for('index'))
            else:
                return render_template('login.html',
                                       title='Sign In',
                                       form=form,
                                       message='wrong username/password')
    return render_template('login.html',
                           title='Sign In',
                           form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/log', methods=['GET', 'POST'])
@login_required
def log_time():
    user = g.user
    form = LogForm()
    if form.validate_on_submit():
        if request.method == 'POST':
            if request.form['submit'] == "log start":
                worksession = Worksession(date = datetime.now().date(),
                              check_in = datetime.now(),
                              check_out = None,
                              user_id = user.id)
                db.session.add(worksession)
                db.session.commit()
            if request.form['submit'] == "log end":
                current_date = datetime.now().date()
                last_session =  user.worksessions.filter_by(date=current_date).group_by('date').all()[0]
                last_session.check_out = datetime.now()
                db.session.add(last_session)
                db.session.commit()
            return redirect(url_for('login'))
    return render_template('log.html',
                           title='Log In',
                           form=form)

@app.route('/plot')
def build_plot():
    plot_url = ''

    return '<img src="data:image/png;base64,{}">'.format(plot_url)
