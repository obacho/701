# -*- coding: utf-8 -*-

from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    workdays = db.relationship('Workday', backref='user', lazy='dynamic')


    def __repr__(self):
        return '<User %r>' % (self.nickname)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, index=True)
    check_out = db.Column(db.Boolean, index=True)
    lunch_time = db.Column(db.Interval, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


    def __repr__(self):
        return '<Event %r>' % (self.date)