from scripts.Total_cases_deaths_plot import plot
from scripts.world_map import world_map_total_cases
from scripts.create_dataset_hist import create_dataset
from scripts.create_dataset_worldmap import create_world_dataset
import pandas as pd
from os.path import dirname, join
from bokeh.io import curdoc
from bokeh.models.widgets import Tabs, Panel
import geopandas as gpd

#install ipython where geopandas is installed
#read covid data
df = pd.read_json(join(dirname(__file__), 'data', 'owid-covid-data.json'))
df = df.T
#read shapefile
shapefile = 'D:\Projects\Bokeh_app\data\countries_110m/ne_110m_admin_0_countries.shp'
gdf = gpd.read_file(shapefile)[['ADMIN', 'ADM0_A3', 'geometry']]
gdf.columns = ['country', 'country_code', 'geometry']
gdf = gdf.drop(gdf.index[159])

df_final = create_dataset(df)
merged_data = create_world_dataset(gdf, df)

p1 = plot(df_final, 'new_cases')
p2 = plot(df_final, 'new_deaths')
p3 = world_map_total_cases(merged_data)

tab1 = Panel(child = p1, title = 'new_cases')
tab2 = Panel(child = p2, title = 'new_deaths')
tab3 = Panel(child=p3, title='world map')
tabs = Tabs(tabs = [tab3, tab2, tab1])
curdoc().add_root(tabs)

