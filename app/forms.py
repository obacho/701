# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 09:19:35 2017

@author: rbomblies
"""

from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField
from wtforms.validators import DataRequired

class StartForm(FlaskForm):
    time = StringField('time', validators=[DataRequired()])

class LogForm(FlaskForm):
    start_time = StringField('start_time', )#validators=[DataRequired()])
    end_time = StringField('end_time', )#validators=[DataRequired()])
    had_lunch = BooleanField('had_lunch', default=True)

class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password')
    remember_me = BooleanField('remember_me', default=True)
