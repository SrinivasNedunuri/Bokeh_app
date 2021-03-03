def world_map_total_cases(merged_data):
    from bokeh.plotting import figure
    from bokeh.models import GeoJSONDataSource, LinearColorMapper, ColorBar, HoverTool, FixedTicker
    from bokeh.palettes import brewer
    from bokeh.models import NumeralTickFormatter
    from bokeh.models.widgets import Select
    from bokeh.layouts import row
    import json

    maxi = round(max(merged_data['total_cases_per_million']), 2)
    # read data to json
    merged_json = json.loads(merged_data.to_json())

    # convert to string like object
    json_data = json.dumps(merged_json)
    geosource = GeoJSONDataSource(geojson=json_data)
    def create_plot(geosource):
        # Define a sequential multi-hue color palette.
        palette = brewer['PuRd'][7]
        palette = palette[::-1]
        color_mapper = LinearColorMapper(palette=palette, low=0, high=maxi)
        # Define custom tick labels for color bar.
        # tick_labels = FixedTicker(ticks = [0,1000,10000,25000,50000,75000,100000])
        # Create color bar.
        color_bar = ColorBar(color_mapper=color_mapper, label_standoff=6, width=500, height=20,
                             border_line_color=None, location=(0, 0), orientation='horizontal',
                             formatter=NumeralTickFormatter(format='0.0a'))

        p = figure(title='Covid-19 Cases Per Million', plot_height=600, plot_width=950, toolbar_location=None)
        p.xgrid.grid_line_color = None
        p.ygrid.grid_line_color = None

        # Add patch renderer to figure.
        path=p.patches('xs', 'ys', source=geosource, fill_color={'field': 'total_cases_per_million', 'transform': color_mapper},
                  line_color='black', line_width=0.25, fill_alpha=1)
        hover = HoverTool(tooltips=[('Country', '@country'), ('Total Cases', '@total_cases{0.00 a}'),
                                    ('Cases Per Million', '@total_cases_per_million{0.00 a}')])
        p.add_tools(hover)
        # Specify figure layout.
        p.add_layout(color_bar, 'below')

        return p,path, color_bar

    def update(attr, old, new):
        feature = selected_feature.value
        p.title.text = 'Covid-19 {} Per Million'.format(feature)
        if feature == 'Total Deaths':
            palette = brewer['YlOrBr'][7]
            palette = palette[::-1]
            ma = round(max(merged_data['total_deaths_per_million']), 2)
            color_mapper = LinearColorMapper(palette=palette, low=0, high=ma)
            col.color_mapper = color_mapper
            path.glyph.fill_color = {'field': 'total_deaths_per_million', 'transform': color_mapper}
            hover = HoverTool(tooltips=[('Country', '@country'), ('Total Deaths', '@total_deaths{0.00 a}'),
                                        ('Deaths Per Million', '@total_deaths_per_million{0.00 a}')])
            p.add_tools(hover)
        else:
            palette = brewer['PuRd'][7]
            palette = palette[::-1]
            ma = round(max(merged_data['total_cases_per_million']), 2)
            color_mapper = LinearColorMapper(palette=palette, low=0, high=ma)
            col.color_mapper = color_mapper
            path.glyph.fill_color = {'field': 'total_cases_per_million', 'transform': color_mapper}
            hover = HoverTool(tooltips=[('Country', '@country'), ('Total Cases', '@total_cases{0.00 a}'),
                                        ('Cases Per Million', '@total_cases_per_million{0.00 a}')])
            p.add_tools(hover)



    selected_feature = Select(title='Options', value='Total Cases', options=['Total Cases', 'Total Deaths'])
    selected_feature.on_change('value', update)

    p, path, col = create_plot(geosource)
    layout = row(selected_feature, p)

    return layout





