import requests
import pandas as pd

from DataCollector.config.constants import API_ENDPOINT
from DataCollector.config.definitions import KEY_URL

url = API_ENDPOINT + "v3/historical-price-full/AAPL?serietype=line&" + KEY_URL
response = requests.get(url).json()["historical"]
data = pd.DataFrame(response)
print(data.columns)
print(data.head())
