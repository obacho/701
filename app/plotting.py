def plot_worksessions(worksessions):
    '''
    plots worksessions
    '''

    import io
    from numpy import arange
    import matplotlib.pyplot as plt
    import matplotlib.dates as dates
    import base64
    from datetime import datetime, timedelta
    img = io.BytesIO()


    def timelines(x, ystart, ystop, ax=plt, color='b', linewidth=2, headwidth=timedelta(hours=1)):
        """Plot timelines at x from ystart to ystop with given color."""
        ax.vlines(x, ystart, ystop, color, lw=2*linewidth)
        ax.hlines(ystart, x+headwidth, x-headwidth, color, lw=linewidth)
        ax.hlines(ystop, x+headwidth, x-headwidth, color, lw=linewidth)

    f, ax = plt.subplots()
    f.set_size_inches([7,5])
    now = datetime.now()
    ax.set_ylim([now.replace(hour=22,minute=0),
                 now.replace(hour=6, minute=0)])
    ax.yaxis.set_major_formatter(dates.DateFormatter('%H:%M'))
    ax.yaxis.set_major_locator(dates.HourLocator(byhour=arange(6,22,3)))
    for sess in worksessions:
        check_in = sess.check_in.replace(year=now.year, month=now.month, day=now.day)
        check_out = sess.check_out.replace(year=now.year, month=now.month, day=now.day)
        print (sess.date,check_in,check_out)
        timelines(sess.date, check_in, check_out, ax)


    plt.savefig(img, format='png')
    img.seek(0)

    return base64.b64encode(img.getvalue()).decode()
