import geopandas as gpd
import pandas as pd
import json
def world_map_total_cases():
    shapefile = 'D:\Projects\Bokeh_app\data\countries_110m/ne_110m_admin_0_countries.shp'

    gdf = gpd.read_file(shapefile)[['ADMIN', 'ADM0_A3', 'geometry']]
    gdf.columns = ['country', 'country_code', 'geometry']
    gdf = gdf.drop(gdf.index[159])

    df = pd.read_json('D:\Projects\Bokeh_app\data/owid-covid-data.json')
    df = df.T
    df['last_entry'] = df['data'].apply(lambda x : x[-1])
    df['total_cases'] = df['last_entry'].apply(lambda x : x.get('total_cases'))
    df['total_deaths'] = df['last_entry'].apply(lambda x : x.get('total_deaths'))
    df['total_cases_per_million'] = df['last_entry'].apply(lambda x : x.get('total_cases_per_million'))
    df['total_deaths_per_million'] = df['last_entry'].apply(lambda x : x.get('total_deaths_per_million'))

    data = df.reset_index().rename(columns = {'index':'Country_code'})[['Country_code', 'location', 'total_cases_per_million']]
    merged_total = data.merge(gdf, left_on= 'Country_code', right_on = 'country_code')
    merged_total.dropna(axis = 0, inplace = True)
    merged_total.reset_index(inplace=True)
    mini = round(min(merged_total['total_cases_per_million']),2)
    maxi = round(max(merged_total['total_cases_per_million']),2)
    #read data to json
    merged_json = json.loads(merged_total.to_json(default_handler=str))
    #convert to string like object
    json_data = json.dumps(merged_json)

    from bokeh.plotting import figure
    from bokeh.models import GeoJSONDataSource, LinearColorMapper, ColorBar
    from bokeh.palettes import brewer
    from bokeh.io import output_file, show, curdoc

    geosource = GeoJSONDataSource(geojson = json_data)
    #print(geosource)
    #Define a sequential multi-hue color palette.
    palette = brewer['YlOrBr'][8]
    palette = palette[::-1]
    color_mapper = LinearColorMapper(palette=palette, low=0, high=maxi)
    # Define custom tick labels for color bar.
    tick_labels = {'0':'0','100': '100', '500': '500', '1000': '1000', '10000': '10000', '25000': '25000', '50000': '50000', '75000': '75000', '100000': '>100000'}

    #Create color bar.
    color_bar = ColorBar(color_mapper=color_mapper, label_standoff=7,width = 500, height = 20,
    border_line_color=None,location = (0,0), orientation = 'horizontal', major_label_overrides = tick_labels)

    p = figure(title = 'Covid-19 Cases Per Million', plot_height = 600 , plot_width = 950, toolbar_location = None)
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None

    #Add patch renderer to figure.
    p.patches('xs','ys', source = geosource, fill_color = {'field':'total_cases_per_million', 'transform' : color_mapper},
              line_color = 'black', line_width = 0.25, fill_alpha = 1)



    #Specify figure layout.
    p.add_layout(color_bar, 'below')

    show(p)
world_map_total_cases()