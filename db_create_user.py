#!venv/bin/python

from app import db, models

default_username = 'seppobacho'
existing_user = models.User.query.filter_by(username=default_username).first()
if not existing_user:
    u = models.User(username=default_username, email='r@inber.to')
    db.session.add(u)
    db.session.commit()

from datetime import datetime, timedelta
from random import randint
now = datetime.now()
for i in range(10):
    itime = now-timedelta(days=i)
    if itime.weekday() in [0,1,2,3,4]:
        ws = models.Worksession(date = itime.date(),
                             check_in = itime.replace(hour=8, minute=15*randint(1,3)),
                             check_out = itime.replace(hour=17, minute=15*randint(1,3)),
                            user_id = 1)
        db.session.add(ws)
        db.session.commit()
