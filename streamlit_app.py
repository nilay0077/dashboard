import streamlit as st
import pandas as pd
import yfinance as yf

# --- Functions ---
@st.cache_data(ttl=3600)  # Cache for 1 hour
def fetch_stock_data(symbol, period="6mo"):
    stock = yf.Ticker(symbol)
    df = stock.history(period=period)
    df = df[["Close"]].rename(columns={"Close": symbol})
    return df

# --- Fetch Data ---
df_tsla = fetch_stock_data("TSLA")
df_spy = fetch_stock_data("SPY")

# --- Merge & Compute Returns ---
df = pd.merge(df_tsla, df_spy, left_index=True, right_index=True, how="inner")

if df.empty:
    st.warning("No data available. Please try again later.")
else:
    returns = df.pct_change().dropna()
    cumulative = (1 + returns).cumprod() - 1
    cumulative.columns = ["TSLA Cumulative Return", "SPY Cumulative Return"]

    # --- Streamlit UI ---
    st.title("📈 TSLA vs S&P 500 (SPY) – Live Return Dashboard")

    st.subheader("Cumulative Returns")
    st.line_chart(cumulative)

    st.subheader("Daily Returns")
    st.line_chart(returns.rename(columns={"TSLA": "TSLA Daily Return", "SPY": "SPY Daily Return"}))

    st.caption("Data via Yahoo Finance · Updates every hour")

