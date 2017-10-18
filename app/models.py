# -*- coding: utf-8 -*-

from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    worksessions = db.relationship('Worksession', backref='user', lazy='dynamic')

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

class Worksession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, index=True)
    check_in = db.Column(db.DateTime, index=True)
    check_out = db.Column(db.DateTime, index=True)
    #lunch_time = db.Column(db.Interval, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


    def __repr__(self):
        return '<session from {} {}:{}>'.format(self.date, 
                                                self.check_in.hour, 
                                                self.check_in.minute)       