# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 08:48:17 2017

@author: rbomblies
"""

from flask import Flask

app = Flask(__name__)
app.config.from_object('config')

from app import views