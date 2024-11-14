import streamlit as st
import pandas as pd
import yfinance as yf
import numpy as np
import statsmodels.api as sm
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

# Set page configuration
st.set_page_config(page_title="Stock Beta & Jensen's Alpha Calculator", layout="wide")

# Add title and description
st.title("Stock Beta & Jensen's Alpha Calculator")
st.markdown("""
This app calculates the Beta coefficient and Jensen's Alpha for a selected stock against a market index.
* **Beta** measures the stock's volatility relative to the market
* **Jensen's Alpha** measures the stock's excess return relative to the market
""")

# Create sidebar inputs
st.sidebar.header("Input Parameters")

# Stock symbol input
stock_symbol = st.sidebar.text_input("Enter Stock Symbol (e.g., AAPL, MSFT)", "AAPL")

# Market index selection
market_indices = {
    "S&P 500": "^GSPC",
    "NASDAQ 100": "^NDX",
    "Dow Jones": "^DJI",
    "Russell 2000": "^RUT"
}
selected_index = st.sidebar.selectbox("Select Market Index", list(market_indices.keys()))

# Date range selection
today = datetime.today()
default_start = today - timedelta(days=5*365)  # 5 years ago
start_date = st.sidebar.date_input("Start Date", default_start)
end_date = st.sidebar.date_input("End Date", today)

# Risk-free rate input
risk_free_rate = st.sidebar.number_input("Annual Risk-free Rate (%)", min_value=0.0, max_value=20.0, value=6.0)

try:
    # Fetch data
    @st.cache_data
    def fetch_data(symbol, start, end):
        return yf.download(symbol, start=start, end=end)

    stock_data = fetch_data(stock_symbol, start_date, end_date)
    market_data = fetch_data(market_indices[selected_index], start_date, end_date)

    # Calculate returns (now using daily returns)
    stock_data['Return'] = stock_data['Adj Close'].pct_change() * 100
    market_data['Return'] = market_data['Adj Close'].pct_change() * 100

    # Create returns dataframe
    returns_df = pd.DataFrame({
        "Stock_Return": stock_data['Return'],
        "Market_Return": market_data['Return']
    }).dropna()

    # Calculate monthly risk-free rate
    risk_free_rate_monthly = (1 + risk_free_rate / 100) ** (1 / 12) - 1

    # Calculate Beta and Jensen's Alpha
    X = returns_df["Market_Return"] - (risk_free_rate_monthly * 100)
    y = returns_df["Stock_Return"] - (risk_free_rate_monthly * 100)
    X = sm.add_constant(X)
    model = sm.OLS(y, X).fit()

    # Display results in main panel
    col1, col2 = st.columns(2)

    with col1:
        st.subheader(f"{stock_symbol} Statistical Results")
        metrics = {
            "Beta": round(model.params["Market_Return"], 4),
            "Jensen's Alpha": round(model.params["const"], 4),
            "R-squared": round(model.rsquared, 4)
        }
        
        for metric, value in metrics.items():
            st.metric(metric, value)

    with col2:
        st.subheader("Interpretation")
        beta = model.params["Market_Return"]
        alpha = model.params["const"]
        
        beta_interpretation = (
            "🔥 **Aggressive**" if beta > 1 
            else "❄️ **Defensive**" if beta < 1 
            else "➡️ **Neutral**"
        )
        
        alpha_interpretation = (
            "📈 **Outperforming**" if alpha > 0 
            else "📉 **Underperforming**" if alpha < 0 
            else "➡️ **Neutral**"
        )

        st.write(f"**Beta ({beta:.4f}):** This stock is {beta_interpretation} compared to the {selected_index}")
        st.write(f"**Alpha ({alpha:.4f}):** This stock is {alpha_interpretation} the market on a risk-adjusted basis")

    # Create visualizations
    st.subheader("Visualizations")

    # Scatter Plot with Regression Line
    fig2 = px.scatter(returns_df, x="Market_Return", y="Stock_Return", 
                     trendline="ols",
                     title=f"{stock_symbol} Returns vs {selected_index} Returns")
    fig2.update_layout(
        height=400,
        xaxis_title=f"{selected_index} Returns (%)",
        yaxis_title=f"{stock_symbol} Returns (%)",
        plot_bgcolor='white',
        title_x=0.5
    )
    st.plotly_chart(fig2, use_container_width=True)

    # Monthly Returns Comparison
    fig3 = go.Figure()
    fig3.add_trace(go.Bar(
        x=returns_df.index,
        y=returns_df['Stock_Return'],
        name=stock_symbol,
        opacity=0.7
    ))
    fig3.add_trace(go.Bar(
        x=returns_df.index,
        y=returns_df['Market_Return'],
        name=selected_index,
        opacity=0.7
    ))
    fig3.update_layout(
        title="Monthly Returns Comparison",
        xaxis_title="Date",
        yaxis_title="Return (%)",
        barmode='group',
        height=400,
        plot_bgcolor='white',
        title_x=0.5
    )
    st.plotly_chart(fig3, use_container_width=True)

except Exception as e:
    st.error(f"An error occurred: {str(e)}")
    st.write("Please check if the stock symbol is valid and try again.")