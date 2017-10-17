# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 08:49:58 2017

@author: rbomblies
"""
from flask import render_template, flash, redirect
from app import app
from .forms import EndForm

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
    form = EndForm()
    return render_template('log.html', 
                           title='Log In',
                           form=form)    