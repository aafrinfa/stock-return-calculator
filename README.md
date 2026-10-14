# Stock Return Calculator

A Python-based application for exploring historical stock prices and calculating daily and cumulative price returns using real market data.

The application allows users to select a stock, choose a date range, inspect historical prices, review summary statistics, and export the results as a CSV file.

## Application Preview


![Stock Return Calculator application overview](screenshots/app-overview.png)

## Live Demo

[Open the Stock Return Calculator](https://stock-return-calculator.streamlit.app/)

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://stock-return-calculator.streamlit.app/)

## Features

- **Historical Market Data:** Retrieve stock price data using Yahoo Finance.
- **Daily Returns:** Calculate percentage changes between consecutive available closing prices.
- **Cumulative Returns:** Measure price performance relative to the first available closing price in the selected period.
- **Summary Statistics:** Review opening-period and latest closing prices, average price, highest and lowest prices, average daily return, and total period return.
- **Interactive Data Exploration:** Select historical data columns to inspect.
- **CSV Export:** Download the selected period's historical data and calculated returns.
- **Input Validation:** Handle invalid date ranges and unavailable market data.
- **Data Caching:** Cache historical data temporarily to reduce repeated requests.

## Technology Stack

- Python
- Streamlit
- Pandas
- yfinance

## Stocks Available

The application currently supports the following stocks:

| Company | Ticker |
|---|---|
| Apple | AAPL |
| Microsoft | MSFT |
| Alphabet | GOOGL |
| Amazon | AMZN |
| Tesla | TSLA |

## Return Calculations

### Daily Return

Daily return measures the percentage change in closing price compared with the previous available trading session.

Formula:

`Daily Return = (Current Close - Previous Close) / Previous Close`

In Pandas, this is calculated using:

`data["Close"].pct_change()`

The first observation has no daily return within the downloaded dataset because there is no previous observation available for comparison.

### Cumulative Price Return

Cumulative price return measures the change in price relative to the first available closing price in the selected period.

Formula:

`Cumulative Return = (Current Close / First Close) - 1`

For example, if the first closing price is $100 and the latest closing price is $110, the cumulative price return is 10%.

This calculation represents price appreciation or depreciation. It does not separately account for dividends, transaction costs, taxes, or inflation.

### Average Daily Return

Average daily return is the arithmetic mean of the calculated daily returns in the selected period.

`Average Daily Return = Mean of Daily Returns`

This is a historical statistic and should not be interpreted as an expected future return.

## Installation and Setup

### Prerequisites

- Python 3.10 or a compatible version
- pip
- An internet connection to retrieve market data

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd stock-return-calculator
```

Replace the placeholder with your actual repository URL.

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Or, in Command Prompt:

```cmd
.venv\Scripts\activate.bat
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
streamlit run app.py
```

Streamlit will provide a local URL, usually `http://localhost:8501`, where you can access the application.

## Data Source

Historical stock data is retrieved through the `yfinance` Python library, which interfaces with Yahoo Finance.

Data availability, historical coverage, and returned values depend on the data provider. The application does not independently verify market data.

## Limitations

- Only a predefined set of stock tickers is currently supported.
- Results depend on the availability and accuracy of data from the external provider.
- The application analyzes historical price movements rather than predicting future prices.
- Returns are price-based and do not represent a complete calculation of an investor's realized return.
- Market holidays and weekends mean that data is available only for trading sessions.

## Future Improvements

- Add support for user-entered stock tickers.
- Visualize historical closing prices and cumulative returns with charts.
- Compare the performance of multiple stocks.
- Add volatility and risk metrics, such as standard deviation and maximum drawdown.
- Include dividend-adjusted total returns.
- Add automated tests for return calculations and date validation.

## Disclaimer

This project is intended for educational and analytical purposes only. It does not provide investment advice or recommendations to buy or sell securities.

## License

No license has been specified yet. Add an appropriate open-source license if you intend to permit others to reuse, modify, or distribute this project.
