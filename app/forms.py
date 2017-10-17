# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 09:19:35 2017

@author: rbomblies
"""

from flask_wtf import Form
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired

class StartForm(Form):
    time = StringField('time', validators=[DataRequired()])

class EndForm(Form):
    time = StringField('time', validators=[DataRequired()])    
    had_lunch = BooleanField('had_lunch', default=True)