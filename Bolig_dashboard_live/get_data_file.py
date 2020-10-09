import pandas as pd
import numpy as np
from datetime import timedelta


def get_data(n, bolig_type_value):
    row_value = ((n / 50) / 100) * (36000 * 4)

    df = pd.read_csv('clean_data/cleaned_df.csv',
                     sep=';', nrows=int(row_value))

    if bolig_type_value == []:
        pass
    else:
        df = df[df['boligtype'].isin(bolig_type_value)]

    df['oprettelsesdato'] = pd.to_datetime(df['oprettelsesdato'])

    return df
