# -*- coding: utf-8 -*-

from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    events = db.relationship('Event', backref='user', lazy='dynamic')

    @property
    def is_authenticated(self):
        return True

    def is_active(self):
        return True        

    @property
    def is_anonymous(self):
        return False        
        
    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3
        
    def __repr__(self):
        return '<User %r>' % (self.nickname)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, index=True)
    time = db.Column(db.DateTime, index=True)
    check_out = db.Column(db.Boolean, index=True)
    #lunch_time = db.Column(db.Interval, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


    def __repr__(self):
        if self.check_out:
            return '<Check-Out at {}>'.format(self.time)
        elif not self.check_out:
            return '<Check-In at {}>'.format(self.time)            