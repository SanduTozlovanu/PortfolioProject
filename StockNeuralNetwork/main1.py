import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import requests

from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.layers import Dense, Dropout, LSTM
from tensorflow.keras.models import Sequential

from publicServer.config.constants import API_ENDPOINT
from publicServer.config.definitions import KEY_URL
RANDOM_CONSTANT = 60
url = API_ENDPOINT + "v3/historical-price-full/AAPL?serietype=line&" + KEY_URL
response = requests.get(url).json()["historical"]
data = pd.DataFrame(response)
data = data[::-1]
data['date'] = pd.to_datetime(data['date'])
data = data.loc[data['date'] >= '2018-04-16']

close_data = data.filter(['close'])
dataset = close_data.values
training = int(np.ceil(len(dataset) * .95))
print(training)

scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(dataset)

train_data = scaled_data[0:int(training), :]
# prepare feature and labels
x_train = []
y_train = []

for i in range(RANDOM_CONSTANT, len(train_data)):
    x_train.append(train_data[i - RANDOM_CONSTANT:i, 0])
    y_train.append(train_data[i, 0])

x_train, y_train = np.array(x_train), np.array(y_train)
x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

model = Sequential()
model.add(LSTM(units=64,
               return_sequences=True,
               input_shape=(x_train.shape[1], 1)))
model.add(LSTM(units=64))
model.add(Dense(32))
model.add(Dropout(0.5))
model.add(Dense(1))
print(model.summary)


model.compile(optimizer='adam',
              loss='mean_squared_error')
history = model.fit(x_train,
                    y_train,
                    epochs=10)

test_data = scaled_data[training - RANDOM_CONSTANT:, :]
x_test = []
y_test = dataset[training:, :]
for i in range(RANDOM_CONSTANT, len(test_data)):
    x_test.append(test_data[i - RANDOM_CONSTANT:i, 0])

x_test = np.array(x_test)
x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

# predict the testing data
predictions = model.predict(x_test)
predictions = scaler.inverse_transform(predictions)

# evaluation metrics
mse = np.mean(((predictions - y_test) ** 2))
print("MSE", mse)
print("RMSE", np.sqrt(mse))

train = data[:training]
test = data[training:]
test['predictions'] = predictions

plt.figure(figsize=(10, 8))
plt.plot(train['date'], train['close'])
plt.plot(test['date'], test[['close', 'predictions']])
plt.title('Apple Stock Close Price')
plt.xlabel('Date')
plt.ylabel("Close")
plt.legend(['Train', 'Test', 'Predictions'])
plt.show()
