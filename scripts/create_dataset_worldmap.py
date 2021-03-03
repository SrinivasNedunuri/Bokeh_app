def create_world_dataset(gdf, df):
    df['last_entry'] = df['data'].apply(lambda x: x[-1])
    df['total_cases'] = df['last_entry'].apply(lambda x: x.get('total_cases'))
    df['total_deaths'] = df['last_entry'].apply(lambda x: x.get('total_deaths'))
    df['total_cases_per_million'] = df['last_entry'].apply(lambda x: x.get('total_cases_per_million'))
    df['total_deaths_per_million'] = df['last_entry'].apply(lambda x: x.get('total_deaths_per_million'))
    data = df.reset_index().rename(columns={'index': 'Country_code'})[
        ['Country_code', 'location', 'total_cases_per_million', 'total_cases', 'total_deaths',
         'total_deaths_per_million']]
    merged_total = gdf.merge(data, right_on='Country_code', left_on='country_code', how='left')[
        ['total_cases_per_million', 'country', 'country_code', 'geometry', 'total_cases', 'total_deaths',
         'total_deaths_per_million']]
    merged_total.fillna(0)
    merged_total.reset_index(inplace=True, drop=True)

    return merged_total