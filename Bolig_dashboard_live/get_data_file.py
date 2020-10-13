import pandas as pd
import numpy as np
from datetime import timedelta


def get_data(n, bolig_type_value, by_value):
    row_value = ((n / 50) / 100) * (36000 * 4)

    df = pd.read_csv('clean_data/cleaned_df.csv',
                     sep=';', nrows=int(row_value))
    df['navn'] = df['navn'].apply(lambda x: x.split(' ')[0])
    df['oprettelsesdato'] = pd.to_datetime(df['oprettelsesdato'])

    if bolig_type_value != [] and by_value != []:
        df = df[(df['boligtype'].isin(bolig_type_value))
                & (df['navn'].isin(by_value))]

    else:

        if bolig_type_value != []:
            df = df[df['boligtype'].isin(bolig_type_value)]

        if by_value != []:
            df = df[df['navn'].isin(by_value)]

    return df
