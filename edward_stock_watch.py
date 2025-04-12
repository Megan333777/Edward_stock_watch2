
import streamlit as st
import yfinance as yf
import requests
from datetime import datetime
from textblob import TextBlob
import pandas as pd

# Your summer short sale + interest watchlist
stocks = {
    "AAL": "American Airlines",
    "DAL": "Delta Air Lines",
    "JBLU": "JetBlue",
    "CAT": "Caterpillar",
    "BYND": "Beyond Meat",
    "KSS": "Kohl's",
    "ULTA": "Ulta Beauty",
    "DIS": "Disney",
    "ABBV": "AbbVie (Skyrizi)",
    "HEN3.DE": "Henkel",
    "GME": "GameStop",
    "F": "Ford Motor Co"
}

st.title("Edward's Market Watch - Summer 2025 Edition")
st.markdown("A calm place to monitor hot stocks, track sentiment, and look for patterns. Built with a moth's wisdom.")

selected = st.multiselect("Select stocks to view:", options=list(stocks.keys()), default=list(stocks.keys())[:3])

for ticker in selected:
    st.subheader(f"{stocks[ticker]} ({ticker})")
    stock = yf.Ticker(ticker)
    data = stock.history(period="7d")
    current_price = data['Close'].iloc[-1]

    st.line_chart(data['Close'])
    st.write(f"**Current Price:** ${current_price:.2f}")

    # Recent news headlines
    st.write("**Latest News Headlines**")
    try:
        news_url = f"https://newsapi.org/v2/everything?q={ticker}&apiKey=YOUR_NEWSAPI_KEY"
        news_data = requests.get(news_url).json()
        if news_data['status'] == 'ok':
            for article in news_data['articles'][:3]:
                sentiment = TextBlob(article['title']).sentiment.polarity
                st.markdown(f"- [{article['title']}]({article['url']}) - Sentiment: {'Positive' if sentiment > 0 else 'Negative' if sentiment < 0 else 'Neutral'}")
        else:
            st.write("News API limit or error.")
    except:
        st.write("Error fetching news.")

    # Reddit buzz tracking (simulated)
    st.write("**Reddit Buzz (Simulated)**")
    reddit_buzz = {
        "AAL": 4, "DAL": 7, "JBLU": 5, "CAT": 2, "BYND": 10,
        "KSS": 3, "ULTA": 1, "DIS": 8, "ABBV": 2, "HEN3.DE": 0,
        "GME": 15, "F": 6
    }
    buzz = reddit_buzz.get(ticker, 0)
    st.write(f"Buzz Score (mentions today): {buzz}")

    # Insider trade and merger alert (mock logic)
    st.write("**AI Alerts**")
    alerts = []
    if buzz > 10:
        alerts.append("High Reddit buzz: possible short squeeze or meme spike.")
    if ticker in ["GME", "BYND", "DAL"]:
        alerts.append("Watch for merger or acquisition rumors.")
    if current_price < data['Close'].mean() * 0.9:
        alerts.append("Price gap detected: downtrend or panic sell.")

    if alerts:
        for alert in alerts:
            st.warning(alert)
    else:
        st.info("No major alerts at this time.")

    st.markdown("---")

st.sidebar.markdown("**Edward's Tips**")
st.sidebar.info("Watch volume surges, merger rumors, and insider trades. Remember: panic is for humans. Patience is for moths.")
