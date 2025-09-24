import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def clean_data(df: pd.DataFrame):
    # Fill missing values with forward fill, then backward fill
    df_clean = df.fillna(method='ffill').fillna(method='bfill')
    return df_clean

def normalize_data(df: pd.DataFrame, columns: list):
    scaler = MinMaxScaler()
    df_scaled = df.copy()
    df_scaled[columns] = scaler.fit_transform(df[columns])
    return df_scaled
