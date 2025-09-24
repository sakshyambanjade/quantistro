import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

def arima_forecast(df: pd.DataFrame, column: str, periods: int = 5):
    series = df[column].astype('float')
    
    # Fit ARIMA model with order (p=5, d=1, q=0) as an example
    model = ARIMA(series, order=(5, 1, 0))
    model_fit = model.fit()
    
    # Forecast next periods
    forecast = model_fit.forecast(steps=periods)
    
    # Return forecast as list
    return forecast.tolist()

# Very fast simple moving average forecast as a fallback when heavy models are unavailable
def simple_ma_forecast(df: pd.DataFrame, column: str, periods: int = 5, window: int = 5):
    series = df[column].astype('float').values
    if len(series) < max(2, window):
        raise ValueError("Not enough data points for simple MA forecast")

    last_values = series[-window:]
    moving_avg = float(pd.Series(last_values).mean())
    return [moving_avg for _ in range(periods)]