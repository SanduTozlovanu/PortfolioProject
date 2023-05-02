import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler

# Load AAPL stock price data
df = pd.read_csv('AAPL_stock_price.csv')

# Convert 'Date' column to datetime type
df['Date'] = pd.to_datetime(df['Date'])

# Sort DataFrame by date
df = df.sort_values('Date')

# Extract 'Close' prices
close_prices = df['Close'].values.reshape(-1, 1)

# Normalize data using Min-Max scaler
scaler = MinMaxScaler()
close_prices_scaled = scaler.fit_transform(close_prices)

# Split data into train and test sets
train_data = close_prices_scaled[:-60]
test_data = close_prices_scaled[-60:]

# Function to create time series dataset
def create_time_series_dataset(data, time_steps):
    X = []
    y = []
    for i in range(len(data) - time_steps):
        X.append(data[i:i+time_steps])
        y.append(data[i+time_steps])
    return np.array(X), np.array(y)

# Define time steps for time series data
time_steps = 60

# Create time series datasets for train and test sets
X_train, y_train = create_time_series_dataset(train_data, time_steps)
X_test, y_test = create_time_series_dataset(test_data, time_steps)

# Build and train LSTM model
model = tf.keras.Sequential([
    tf.keras.layers.LSTM(units=50, return_sequences=True, input_shape=(time_steps, 1)),
    tf.keras.layers.LSTM(units=50),
    tf.keras.layers.Dense(units=1)
])
model.compile(optimizer='adam', loss='mean_squared_error')
model.fit(X_train, y_train, epochs=100, batch_size=32)

# Make predictions for next 5 years
future_dates = pd.date_range(start=df['Date'].iloc[-1] + pd.DateOffset(days=1), periods=5*365, closed='right')
future_dates = pd.DataFrame({'Date': future_dates})
future_close_prices_scaled = scaler.transform(test_data[-time_steps:])
X_future, _ = create_time_series_dataset(future_close_prices_scaled, time_steps)
y_future = model.predict(X_future)
y_future = scaler.inverse_transform(y_future)

# Add future predictions to DataFrame
future_dates['Close'] = y_future
df = pd.concat([df, future_dates], ignore_index=True)

# Print DataFrame with future predictions
print(df.tail(1826))  # Print last 5 years of data