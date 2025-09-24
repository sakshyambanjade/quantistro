import numpy as np
import pandas as pd
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler


def lstm_forecast(df: pd.DataFrame, column: str, forecast_steps: int = 5, look_back: int = 10):
    # Guards
    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found in data")
    if len(df) < 3:
        raise ValueError("Not enough data points to train LSTM")

    # Cap look_back to available data size - 1
    max_look_back = max(2, min(look_back, len(df) - 1))

    # Normalize data
    scaler = MinMaxScaler(feature_range=(0, 1))
    data_scaled = scaler.fit_transform(df[[column]])

    # Prepare training datasets using sliding window
    X, y = [], []
    for i in range(len(data_scaled) - max_look_back):
        X.append(data_scaled[i:i + max_look_back, 0])
        y.append(data_scaled[i + max_look_back, 0])
    if len(X) == 0:
        raise ValueError("Not enough data to create training sequences")
    X, y = np.array(X), np.array(y)
    X = np.reshape(X, (X.shape[0], X.shape[1], 1))

    # Small model for CPU speed
    np.random.seed(42)
    tf.random.set_seed(42)
    model = Sequential()
    model.add(LSTM(50, return_sequences=False, input_shape=(X.shape[1], 1)))
    model.add(Dense(1))
    model.compile(optimizer="adam", loss="mean_squared_error")

    # Train briefly
    model.fit(X, y, epochs=3, batch_size=8, verbose=0)

    # Forecast future values
    last_sequence = data_scaled[-max_look_back:].reshape(1, max_look_back, 1)
    forecasted = []
    current_sequence = last_sequence.copy()
    for _ in range(forecast_steps):
        pred = model.predict(current_sequence, verbose=0)[0][0]
        forecasted.append(pred)
        current_sequence = np.append(current_sequence[:, 1:, :], [[[pred]]], axis=1)

    # Inverse scale back to price domain
    forecasted = scaler.inverse_transform(np.array(forecasted).reshape(-1, 1)).flatten()
    return forecasted.tolist()
