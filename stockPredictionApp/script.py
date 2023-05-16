import yfinance as yf
from prophet import Prophet
from prophet.plot import plot_plotly


def predict(ticker: str):
    period = 5 * 365
    data = yf.download(ticker, period="max")
    data.reset_index(inplace=True)
    df_train = data[['Date', 'Close']]
    df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

    m = Prophet()
    m.fit(df_train)
    future = m.make_future_dataframe(periods=period)
    forecast = m.predict(future)
    fig1 = plot_plotly(m, forecast)
    return fig1.to_json()

print(predict("AMZN"))
