import io
from numpy import arange
import matplotlib.pyplot as plt
import matplotlib.dates as dates
import base64
from datetime import datetime, timedelta
from string import Template

def timelines(x, ystart, ystop, ax=plt, color='#0b5789', linewidth=6, headwidth=timedelta(hours=5)):
    """Plot timelines at x from ystart to ystop with given color."""
    ax.vlines(x, ystart, ystop, color, lw=linewidth)
    ax.hlines(ystart, x+headwidth, x-headwidth, color, lw=linewidth)
    ax.hlines(ystop, x+headwidth, x-headwidth, color, lw=linewidth)

class DeltaTemplate(Template):
    delimiter = "%"

def strfdelta(tdelta, fmt):
    d = {"D": tdelta.days}
    d["H"], rem = divmod(tdelta.seconds, 3600)
    d["M"], d["S"] = divmod(rem, 60)
    t = DeltaTemplate(fmt)
    return t.substitute(**d)

def plot_worksessions(worksessions):
    '''
    plots worksessions
    '''

    img = io.BytesIO()

    f, ax = plt.subplots()
    f.set_size_inches([7,5])
    for spine in ['top', 'bottom', 'left', 'right']:
        ax.spines[spine].set_visible(False)
    ax.xaxis.set_major_formatter(dates.DateFormatter('%a\n%-d.%-m.'))
    now = datetime.now()
    ax.set_ylim([now.replace(hour=20,minute=0),
                 now.replace(hour=7, minute=0)])
    ax.yaxis.set_major_formatter(dates.DateFormatter('%H:%M'))
    ax.yaxis.set_major_locator(dates.HourLocator(byhour=arange(6,22,3)))
    ax.grid(axis='y')
    for sess in worksessions:
        date = datetime.combine(sess.date, datetime.min.time())
        check_in = sess.check_in.replace(year=now.year, month=now.month, day=now.day)
        check_out = sess.check_out.replace(year=now.year, month=now.month, day=now.day)
        workhours = check_out - check_in
        timelines(date, check_in, check_out, ax)
        ax.text(date+timedelta(hours=3), check_in+workhours/2, strfdelta(workhours, '%H:%M'), rotation=90)


    plt.savefig(img, format='png', bbox_inches='tight', transparent=True)
    img.seek(0)

    return base64.b64encode(img.getvalue()).decode()
