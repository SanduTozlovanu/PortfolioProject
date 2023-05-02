import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import requests

from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.layers import Dense, Dropout, LSTM
from tensorflow.keras.models import Sequential

from DataCollector.config.constants import API_ENDPOINT
from DataCollector.config.definitions import KEY_URL

url = API_ENDPOINT + "v3/historical-price-full/AAPL?serietype=line&" + KEY_URL
response = requests.get(url).json()["historical"]
data = pd.DataFrame(response)
data['date'] = pd.to_datetime(data['date'])
data = data.loc[data['date'] <= '2022-04-16']

scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(data['close'].values.reshape(-1, 1))

prediction_days = 60

x_train, y_train = [], []

for x in range(prediction_days, len(scaled_data)):
    x_train.append(scaled_data[x - prediction_days:x, 0])
    y_train.append(scaled_data[x, 0])

x_train, y_train = np.array(x_train), np.array(y_train)
x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

# create neural network

model = Sequential()

model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
model.add(Dropout(0.2))
model.add(LSTM(units=50, return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(units=50))
model.add(Dropout(0.2))
model.add(Dense(units=1))

model.compile(optimizer="adam", loss='mean_squared_error')
model.fit(x_train, y_train, epochs=1)

# testing the model

data_test = pd.DataFrame(response)
data_test['date'] = pd.to_datetime(data_test['date'])
data_test = data_test.loc[data_test['date'] >= '2022-04-16']
actual_prices = data_test['close'].values

total_dataset = pd.concat((data["close"], data_test["close"]), axis=0)

model_inputs = total_dataset[len(total_dataset) - len(data_test) - prediction_days:].values
model_inputs = model_inputs.reshape(-1, 1)
model_inputs = scaler.fit_transform(model_inputs)

x_test = []

for x in range(prediction_days, len(model_inputs)):
    x_test.append(model_inputs[x-prediction_days:x, 0])

x_test = np.array(x_test)
x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

prediction_prices = model.predict(x_test)
prediction_prices = scaler.inverse_transform(prediction_prices)

plt.plot(actual_prices, color='black', label="Actual Prices")
plt.plot(prediction_prices, color='green', label='Predicted Prices')
plt.title(f"APPL price prediction")
plt.xlabel("Time")
plt.ylabel("Price")
plt.legend(loc='upper left')
plt.show()



