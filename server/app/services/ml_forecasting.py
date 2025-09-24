import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

def create_lag_features(df, lag=5):
    for i in range(1, lag + 1):
        df[f'lag_{i}'] = df['close'].shift(i)
    return df.dropna()

def random_forest_forecast(df: pd.DataFrame, forecast_steps=5):
    df = create_lag_features(df)
    
    X = df.drop(columns=['close'])
    y = df['close']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
    
    model = RandomForestRegressor(n_estimators=100)
    model.fit(X_train, y_train)
    
    # Forecast next points recursively
    last_known = X_test.iloc[-1].copy()
    forecasts = []
    for _ in range(forecast_steps):
        pred = model.predict([last_known])[0]
        forecasts.append(pred)
        # Update features for next prediction
        last_known = last_known.shift(1)
        last_known['lag_1'] = pred
    
    return forecasts
