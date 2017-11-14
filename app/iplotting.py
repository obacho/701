from datetime import datetime, timedelta
from bokeh.models import (HoverTool, FactorRange, Plot, LinearAxis, Grid,
                          Range1d)
from bokeh.models.glyphs import VBar
from bokeh.plotting import figure
#from bokeh.plotting import Bar
from bokeh.embed import components
from bokeh.models.sources import ColumnDataSource

def create_hover_tool():
    """Generates the HTML for the Bokeh's hover data tool on our graph."""
    hover_html = """
      <div>
        <span class="hover-tooltip">@hours hours</span>
      </div>
      <div>
        <span class="hover-tooltip">@check_in to @check_out</span>
      </div>
    """
    return HoverTool(tooltips=hover_html)

def create_bar_chart(data, title, x_name, y_name, hover_tool=None,
                     width=1200, height=300):
    """Creates a bar chart plot with the exact styling for the centcom
       dashboard. Pass in data as a dictionary, desired plot title,
       name of x axis, y axis and the hover tool HTML.
    """
    source = ColumnDataSource(data)
    #xdr = FactorRange(factors=sorted([str(x) for x in data[x_name]]))
    xdr = FactorRange(factors=data[x_name])
    ydr = Range1d(start=0,end=max(data[y_name])*1.5)

    tools = []
    if hover_tool:
        tools = [hover_tool,]

    plot = figure(title=title, x_range=xdr, y_range=ydr, plot_width=width,
                  plot_height=height, h_symmetry=False, v_symmetry=False,
                  min_border=0, toolbar_location="above", tools=tools,
                  responsive=True, outline_line_color="#666666")

    glyph = VBar(x=x_name, top=y_name, bottom=0, width=.8,
                 fill_color="#e12127")
    plot.add_glyph(source, glyph)

    xaxis = LinearAxis()
    yaxis = LinearAxis()

    plot.add_layout(Grid(dimension=0, ticker=xaxis.ticker))
    plot.add_layout(Grid(dimension=1, ticker=yaxis.ticker))
    plot.toolbar.logo = None
    plot.min_border_top = 0
    plot.xgrid.grid_line_color = None
    plot.ygrid.grid_line_color = "#999999"
    plot.yaxis.axis_label = x_name
    plot.ygrid.grid_line_alpha = 0.1
    plot.xaxis.axis_label = "axis_label"
    plot.xaxis.major_label_orientation = 1
    return plot

def iplot_worksessions(worksessions):
    ''' plot worksession time
        with bokeh
    '''

    # generate datapoints
    now = datetime.now()
    data = {'date': [], 'hours':[], 'check_in':[], 'check_out':[]}
    for sess in worksessions:
        date = datetime.combine(sess.date, datetime.min.time())
        check_in = sess.check_in.replace(year=now.year, month=now.month, day=now.day)
        if sess.check_out:
            check_out = sess.check_out.replace(year=now.year, month=now.month, day=now.day)
        else:
            check_out = now
        data['date'].append('{}.{}.'.format(date.day, date.month))
        data['hours'].append((check_out - check_in).seconds/3600.)
        data['check_in'].append('{}:{}'.format(check_in.hour, check_in.minute))
        data['check_out'].append('{}:{}'.format(check_out.hour, check_out.minute))
    print (data)

    hover = create_hover_tool()
    plot = create_bar_chart(data, "Hours of work per day", "date",
                            "hours", hover)
    script, div = components(plot)
    return script, div
