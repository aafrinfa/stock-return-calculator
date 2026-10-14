import datetime

import pandas as pd
import streamlit as st
import yfinance as yf


st.set_page_config(
    page_title="Stock Return Calculator",
    page_icon=None,
    layout="wide",
)

st.title("Stock Return Calculator")
st.caption("Historical price data and return analysis")

st.markdown(
    """
    Analyze historical stock prices and calculate daily and cumulative
    returns over a selected period. Choose a stock, specify a date range,
    and review the results using the data table and summary statistics.

    *Data is provided by Yahoo Finance. This application is for educational
    purposes and does not provide investment advice.*
    """
)

POPULAR_TICKERS = {
    "Apple (AAPL)": "AAPL",
    "Microsoft (MSFT)": "MSFT",
    "Alphabet (GOOGL)": "GOOGL",
    "Amazon (AMZN)": "AMZN",
    "Tesla (TSLA)": "TSLA",
}


@st.cache_data(ttl=900)
def fetch_stock_data(ticker, start_date, end_date):
    """Fetch historical stock prices for the selected date range."""
    data = yf.download(
        ticker,
        start=start_date,
        end=end_date + datetime.timedelta(days=1),
        progress=False,
    )

    if data.empty:
        return pd.DataFrame()

    # Handle MultiIndex columns returned by some yfinance versions.
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    if "Close" not in data.columns:
        return pd.DataFrame()

    # Retain rows with valid closing prices.
    data = data.dropna(subset=["Close"]).copy()

    # Keep observations within the requested date range.
    data = data.loc[
        (data.index.date >= start_date)
        & (data.index.date <= end_date)
    ]

    return data


with st.sidebar:
    st.header("Analysis Settings")

    selected_stock = st.selectbox(
        "Stock",
        options=list(POPULAR_TICKERS.keys()),
    )

    ticker = POPULAR_TICKERS[selected_stock]

    today = datetime.date.today()
    default_start = today - datetime.timedelta(days=365)

    start_date = st.date_input(
        "Start date",
        value=default_start,
        max_value=today,
    )

    end_date = st.date_input(
        "End date",
        value=today,
        max_value=today,
    )

    calculate = st.button(
        "Calculate returns",
        type="primary",
        use_container_width=True,
    )


if calculate:
    if start_date > end_date:
        st.error("The start date must be on or before the end date.")
        st.stop()

    with st.spinner("Fetching historical stock data..."):
        data = fetch_stock_data(ticker, start_date, end_date)

    if data.empty:
        st.error(
            "No valid stock price data was found for the selected "
            "stock and date range. Please try another range."
        )
        st.stop()

    # Calculate daily percentage changes.
    data["Daily Return"] = data["Close"].pct_change()

    # Calculate cumulative price return relative to the first
    # available closing price in the selected period.
    first_close = data["Close"].iloc[0]
    data["Cumulative Return"] = data["Close"] / first_close - 1

    st.session_state["stock_data"] = data
    st.session_state["stock_name"] = selected_stock
    st.session_state["start_date"] = start_date
    st.session_state["end_date"] = end_date


if "stock_data" in st.session_state:
    data = st.session_state["stock_data"]
    stock_name = st.session_state["stock_name"]
    start_date = st.session_state["start_date"]
    end_date = st.session_state["end_date"]

    st.divider()

    st.subheader(f"{stock_name} — Historical Analysis")
    st.caption(
        f"Period: {start_date:%d %b %Y} to {end_date:%d %b %Y}"
    )

    first_close = data["Close"].iloc[0]
    last_close = data["Close"].iloc[-1]
    total_return = (last_close / first_close) - 1
    average_daily_return = data["Daily Return"].mean()

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "First closing price",
        f"${first_close:,.2f}",
    )

    col2.metric(
        "Latest closing price",
        f"${last_close:,.2f}",
        delta=f"{total_return:.2%} total return",
    )

    col3.metric(
        "Average daily return",
        f"{average_daily_return:.4%}"
        if pd.notna(average_daily_return)
        else "N/A",
    )

    st.divider()

    st.subheader("Historical Price and Returns")

    display_columns = [
        "Close",
        "Daily Return",
        "Cumulative Return",
    ]

    st.dataframe(
        data[display_columns].style.format(
            {
                "Close": "${:,.2f}",
                "Daily Return": "{:.4%}",
                "Cumulative Return": "{:.4%}",
            },
            na_rep="—",
        ),
        use_container_width=True,
    )

    st.subheader("Return Summary")

    summary = pd.DataFrame(
        {
            "Metric": [
                "First closing price",
                "Latest closing price",
                "Highest closing price",
                "Lowest closing price",
                "Average closing price",
                "Average daily return",
                "Total period return",
                "Number of trading sessions",
            ],
            "Value": [
                f"${data['Close'].iloc[0]:,.2f}",
                f"${data['Close'].iloc[-1]:,.2f}",
                f"${data['Close'].max():,.2f}",
                f"${data['Close'].min():,.2f}",
                f"${data['Close'].mean():,.2f}",
                (
                    f"{average_daily_return:.4%}"
                    if pd.notna(average_daily_return)
                    else "N/A"
                ),
                f"{total_return:.4%}",
                f"{len(data):,}",
            ],
        }
    )

    st.dataframe(
        summary,
        hide_index=True,
        use_container_width=True,
    )

    st.subheader("Column Reference")

    column_descriptions = {
        "Open": "Opening price for the trading session.",
        "High": "Highest recorded price during the session.",
        "Low": "Lowest recorded price during the session.",
        "Close": "Closing price reported by the data provider.",
        "Volume": "Number of shares traded during the session.",
        "Daily Return": (
            "Percentage change in closing price compared "
            "with the previous available trading session."
        ),
        "Cumulative Return": (
            "Price return relative to the first available "
            "closing price in the selected period."
        ),
    }

    with st.expander("View column definitions"):
        for column in data.columns:
            description = column_descriptions.get(
                str(column),
                "Historical market data provided by Yahoo Finance.",
            )
            st.markdown(f"**{column}** — {description}")

    st.subheader("Explore Historical Data")

    available_columns = list(data.columns)

    default_columns = (
        ["Close"]
        if "Close" in available_columns
        else available_columns[:1]
    )

    selected_columns = st.multiselect(
        "Choose columns to display",
        options=available_columns,
        default=default_columns,
    )

    if selected_columns:
        st.dataframe(
            data[selected_columns],
            use_container_width=True,
        )

    csv_data = data.to_csv().encode("utf-8")

    st.download_button(
        label="Download historical data (CSV)",
        data=csv_data,
        file_name=f"{ticker}_{start_date}_{end_date}.csv",
        mime="text/csv",
    )

else:
    st.info(
        "Select a stock and date range in the sidebar, "
        "then click Calculate returns to begin."
    )
