import yfinance as yf
from prophet import Prophet
from prophet.plot import plot_plotly, plot_components_plotly
import pandas as pd
import plotly.graph_objects as go

def get_all_tickers(ticker):
    notes = []
    ticks = yf.Ticker(ticker)
    if ticker and ticks.history().empty:
        notes.append(f'{ticker.upper()} is not available')
    return ticks, notes

def candlestick(tick, period, name):
    data = tick.history(period=period).reset_index()
    fig = go.Figure(data=[go.Candlestick(x=data['Date'],
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'])])
    fig.update_layout(title=f'Historical Data of {name.upper()} Stock')
    return data, fig

def forecasting(data,period):
    df = data[['Date','Close']].rename(columns={'Date':'ds','Close':'y'})
    df['ds'] = df['ds'].dt.tz_localize(None)
    m = Prophet()
    m.fit(df)
    future = m.make_future_dataframe(periods=period)
    forecast = m.predict(future)
    fig1 = plot_plotly(m,forecast)
    fig2 = plot_components_plotly(m,forecast)
    return fig1, fig2