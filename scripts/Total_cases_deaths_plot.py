from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from bokeh.models import HoverTool
from bokeh.models import NumeralTickFormatter
from bokeh.models import Column
from bokeh.models.widgets import Select, DateRangeSlider
from bokeh.layouts import row
from datetime import datetime


def plot(df, feauture):

    def create_plot(source,country, feauture):
        hover = HoverTool(tooltips=[("Date", "@date{%F}"), (feauture, str('@'+feauture))],
                      formatters = {'@date':'datetime'})

        p = figure(plot_width=900, plot_height=500,x_axis_type="datetime",
                   title="Total Covid-19 {} in {} by date".format(feauture, country),
                    toolbar_location='above')

        p.line(x='date', y=feauture, line_width=1, source=source,
               line_color="black")
        p.vbar(x='date', top = feauture, line_width = 1, source = source, fill_color = 'orange', hover_fill_color = 'grey',
               hover_fill_alpha = 1)

        p.add_tools(hover)
        p.xaxis.axis_label = 'Date'
        p.yaxis.axis_label = 'Number of {}'.format(feauture)
        p.axis.axis_label_text_font_style = 'bold'
        p.yaxis.formatter = NumeralTickFormatter(format = '0.0a')
        p.background_fill_color = "beige"

        return p


    def update(attr, old, new):
        country = country_select.value
        new_df = df[df['location'] == country]
        start = datetime.fromtimestamp(date_select.value[0] / 1000)
        end = datetime.fromtimestamp(date_select.value[1] / 1000)
        new_df = new_df[new_df['date'] >= start]
        new_df = new_df[new_df['date'] <= end]
        new_src = ColumnDataSource(new_df)
        source.data.update(new_src.data)
        p.title.text = 'Total covid-19 {} in {}'.format(feauture, country)




    countries = list(df['location'].unique())

    country_select = Select(title = 'Country', value = 'world', options = countries)
    country_select.on_change('value', update)

    date_select = DateRangeSlider(title = 'Date Range', start = min(df['date']), end = max(df['date']),
                              value = (min(df['date']), max(df['date'])), step = 15)
    date_select.on_change('value', update)


    initial_country = country_select.value
    source = ColumnDataSource(df[df['location'] == initial_country])

    p = create_plot(source, initial_country, feauture)

    controls = Column(country_select, date_select)

    layout = row(controls, p)
    return layout