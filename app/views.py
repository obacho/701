# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 08:49:58 2017

@author: rbomblies
"""
from flask import render_template, redirect, url_for, request, g, session
from flask_login import login_user, logout_user, current_user, login_required
from datetime import datetime
from app import app, db, lm
from .forms import LogForm, LoginForm
from .models import User, Event

@app.route('/')
@app.route('/index')
@login_required
def index():
    user = g.user
    #user = {'nickname': 'Rainberto I.'}  # fake user    
    logs = [
             {'day': '16.10.17',
             'times': {'start': '8:00', 
                      'end':   '17:30'}
              },
             {'day': '17.10.17',
             'times': {'start': '8:15', 
                      'end':   '17:15'}
              },]
    return render_template('index.html',
                           title='Home',
                           user=user,
                           logs=logs)


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
            nickname = form.nickname.data
            session.pop('remember_me', None)

            user = User.query.filter_by(nickname=nickname).first()
            if user:
                login_user(user, remember = form.remember_me.data)
                return redirect(url_for('index'))
            else:
                return redirect(url_for('login'))
    return render_template('login.html', 
                           title='Sign In',
                           form=form)    

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
    
@app.route('/log', methods=['GET', 'POST'])
def log_time():
    form = LogForm()
    if form.validate_on_submit():
        if request.method == 'POST':
            if request.form['submit'] == "log start":
                event = Event(date = datetime.now().date(),
                              time = datetime.now(), 
                              check_out = False,
                              user_id = 1)
                db.session.add(event)
                db.session.commit()
            if request.form['submit'] == "log end":
                event = Event(date = datetime.now().date(),
                              time = datetime.now(), 
                              check_out = True,
                              user_id = 1)
                db.session.add(event)
                db.session.commit()                
            return redirect(url_for('login'))
    return render_template('log.html', 
                           title='Log In',
                           form=form)