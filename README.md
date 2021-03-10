# Interactive visualization dashboard of covid-19 data using bokeh

<h2>Data</h2> 
Complete COVID-19 dataset is a collection of the COVID-19 data maintained by Our World in Data. It is updated daily and includes data on confirmed cases, deaths, and testing. Data can be found here <ref>https://ourworldindata.org/coronavirus-source-data<ref> 

<h2>Directory Layout</h2>

```bash
Bokeh_app
├── data
│   ├── countries_110m
│   │   ├── ne_110m_admin_0_countries.README.html
│   │   ├── ne_110m_admin_0_countries.VERSION.txt
│   │   ├── ne_110m_admin_0_countries.cpg
│   │   ├── ne_110m_admin_0_countries.dbf
│   │   ├── ne_110m_admin_0_countries.prj
│   │   ├── ne_110m_admin_0_countries.shp
│   │   └── ne_110m_admin_0_countries.shx
│   └── owid-covid-data.csv
├── scripts
│   ├── __init__
│   ├── create_dataset_hist.py
│   ├── create_dataset_worldmap.py
│   ├── Total_cases_deaths_plot.py
│   ├── world_map.py  
|
└── main.py
```
<h2>Start bokeh server</h2>
open up a command line interface (I prefer Git Bash but any one will work), change to the directory containing bokeh_app and run:  
`bokeh serve --show Bokeh_app` <br/>
the application will automatically open in our browser at the address `http://localhost:5006/bokeh_app`. We can then access the application and explore our dashboard!
