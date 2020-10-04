import pandas as pd
import numpy as np
from datetime import timedelta


def get_data(n, bolig_type_value):
    # random_num = np.random.uniform(2.2, 2.5, size=1)[0]
    # row_value = ((n / random_num) / 100) * 36000
    row_value = ((n / 50) / 100) * 36000

    df = pd.read_csv('clean_data/cleaned_df.csv',
                     sep=';', nrows=int(row_value))

    if bolig_type_value == []:
        pass
    else:
        df = df[df['boligtype'].isin(bolig_type_value)]

    df['oprettelsesdato'] = pd.to_datetime(df['oprettelsesdato'])

    return df
