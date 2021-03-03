import pandas as pd
def create_dataset(df):
    df['by_day'] = df['continent']
    for idx, row in df.iterrows():
        df['by_day'][idx] = pd.DataFrame(row['data'], index=[idx] * len(row['data']))
        if idx == 'AFG':
            df1 = df['by_day'][idx]
        else:
            df1 = pd.concat([df1, df['by_day'][idx]])
    df1 = df1[['date', 'new_cases', 'new_deaths']]
    final_df = df1.join(df[['location']], how='inner').fillna(0).reset_index(drop=True)
    final_df['date'] = pd.to_datetime(final_df['date'])
    df_world = final_df.groupby('date')[['new_cases', 'new_deaths']].sum().reset_index()
    df_world['location'] = ['world'] * df_world.shape[0]
    df_final = pd.concat([df_world, final_df])
    return df_final