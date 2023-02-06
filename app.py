import streamlit as st
from packages import get_all_tickers, candlestick, forecasting

periods = {
    '1 day':'1d',
    '5 days':'5d',
    '1 month':'1mo',
    '3 months':'3mo',
    '6 months':'6mo',
    '1 year':'1y',
    '2 years':'2y',
    '5 years':'5y',
    '10 years':'10y',
    'Year to date':'ytd',
    'Max':'max'
}

st.set_page_config(
    layout='wide'
)

st.title('Stocks Forecasting')

ticker = st.text_input('Input Ticker')

ticks,notes = get_all_tickers(ticker)

if notes:
    st.write(notes[0])

if ticker and not notes:
    do_forecast = st.sidebar.checkbox('Show Forecasting')
    opt = st.sidebar.selectbox('Select Historical Period', periods.keys(),index=7)
    data, fig = candlestick(ticks,periods[opt],ticker)

    st.plotly_chart(fig, use_container_width=True)

    if do_forecast:
        fd = st.sidebar.slider('Select Forecasting Period', min_value=1, max_value=365, value=60)
        fig1,fig2 = forecasting(data, fd)

        col1, col2 = st.columns(2)

        with col1:
            st.plotly_chart(fig1, use_container_width=True)

        with col2:
            st.plotly_chart(fig2, use_container_width=True)
