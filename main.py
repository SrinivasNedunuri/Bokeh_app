from scripts.Total_cases_deaths_plot import plot
from scripts.world_map import world_map_total_cases
import pandas as pd
from os.path import dirname, join
from bokeh.io import curdoc
from bokeh.models.widgets import Tabs, Panel
import geopandas as gpd

#install ipython where geopandas is installed

df = pd.read_json(join(dirname(__file__), 'data', 'owid-covid-data.json'))
df = df.T



df['by_day'] = df['continent']
for idx, row in df.iterrows():
    df['by_day'][idx] = pd.DataFrame(row['data'], index = [idx]*len(row['data']))
    if idx == 'AFG':
        df1 = df['by_day'][idx]
    else:
        df1 = pd.concat([df1, df['by_day'][idx]])

df1 = df1[['date', 'total_cases','new_cases','total_cases_per_million', 'new_cases_per_million', 'total_deaths','new_deaths', 'total_deaths_per_million','new_deaths_per_million']]
final_df = df1.join(df[['location']], how = 'inner')
final_df = final_df.set_index(['date', final_df.index])
final_df.fillna(0, inplace = True)
final_df = final_df[['new_cases', 'new_deaths','location']]
final_df.reset_index(inplace = True)
final_df.drop('level_1', axis = 1, inplace = True)
final_df['date'] = pd.to_datetime(final_df['date'])
df_world = final_df.groupby('date')[['new_cases', 'new_deaths']].sum()
df_world = df_world.reset_index()
df_world['location'] = ['world']*df_world.shape[0]
df_final = pd.concat([df_world, final_df])



p1 = plot(df_final, 'new_cases')
p2 = plot(df_final, 'new_deaths')
tab1 = Panel(child = p1, title = 'new_cases')
tab2 = Panel(child = p2, title = 'new_deaths')
tabs = Tabs(tabs = [tab1, tab2])
curdoc().add_root(tabs)

