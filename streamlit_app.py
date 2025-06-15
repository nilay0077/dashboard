import streamlit as st
import pandas as pd
import requests

API_KEY = 'US2KWIJEBGL8WFB3'
BASE_URL = 'https://www.alphavantage.co/query'

# --- Functions ---
def fetch_stock_data(symbol):
    url = f"{BASE_URL}?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}&outputsize=compact"
    r = requests.get(url)
    data = r.json()
    ts = data.get("Time Series (Daily)", {})
    df = pd.DataFrame({date: float(day["4. close"]) for date, day in ts.items()}, index=[symbol]).T
    df.index = pd.to_datetime(df.index)
    return df.sort_index()

# --- Fetch Data ---
df_tsla = fetch_stock_data("TSLA")
df_spy = fetch_stock_data("SPY")

# --- Merge & Compute Returns ---
df = pd.merge(df_tsla, df_spy, left_index=True, right_index=True, how='inner')
returns = df.pct_change().dropna()
cumulative = (1 + returns).cumprod() - 1
cumulative.columns = ["TSLA Cumulative Return", "SPY Cumulative Return"]

# --- Streamlit UI ---
st.title("📈 TSLA vs S&P 500 (SPY) – Live Return Dashboard")

st.subheader("Cumulative Returns")
st.line_chart(cumulative)

st.subheader("Daily Returns")
st.line_chart(returns.rename(columns={"TSLA": "TSLA Daily Return", "SPY": "SPY Daily Return"}))

st.caption("Data via Alpha Vantage · Updates every time you reload the page")
