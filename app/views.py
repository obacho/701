# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 08:49:58 2017

@author: rbomblies
"""
from flask import render_template, flash, redirect, url_for, request
from datetime import datetime
from app import app, db
from .forms import LogForm
from .models import Event

@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'Rainberto I.'}  # fake user    
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
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LogForm()
    if form.validate_on_submit():
        if request.method == 'POST':
            if request.form['submit'] == "log start":
                event = Event(time=datetime.now(), 
                              check_out=False,
                              user_id = 0)
                db.session.add(event)
                db.session.commit()
            if request.form['submit'] == "log end":
                event = Event(time=datetime.now(), 
                              check_out=True,
                              user_id = 0)
                db.session.add(event)
                db.session.commit()                
            return redirect(url_for('login'))
    return render_template('log.html', 
                           title='Log In',
                           form=form)