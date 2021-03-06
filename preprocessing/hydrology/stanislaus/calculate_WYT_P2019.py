import os
import pandas as pd


def calculate_WYT_P2019(scenario_path):
    def assign_WYT(row):
        if row['flow'] <= 140000:
            x = 1
        elif row['flow'] <= 320000:
            x = 2
        elif row['flow'] <= 400000:
            x = 3
        elif row['flow'] <= 500000:
            x = 4
        else:
            x = 5
        return x

    fnf_path = os.path.join(scenario_path, 'preprocessed', 'full_natural_flow_daily_mcm.csv')
    df = pd.read_csv(fnf_path, names=['date', 'flow'], index_col=0, header=0, parse_dates=[0])  # mcm
    df['year'] = df.index.year
    df1 = df[df.index.map(lambda x: x.month in [4, 5, 6, 7])]
    df2 = df1.groupby('year').sum() / 1.2335 * 1000
    df2.index.name = 'WY'
    df2['WYT'] = df2.apply(lambda row: assign_WYT(row), axis=1)
    df2.drop('flow', axis=1, inplace=True)
    outpath = os.path.join(scenario_path, 'preprocessed', 'WYT_P2019.csv')
    df2.to_csv(outpath)
