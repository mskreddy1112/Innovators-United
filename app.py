# import yfinance as yf
# import pandas as pd
# from datetime import datetime
# from dateutil.relativedelta import relativedelta
# import numpy as np
# from flask import Flask, render_template, request
# import pandas as pd

# app = Flask(__name__)

# # Function to calculate correlation
# def calculate_correlation(stock_ticker):
#     tickers = ['AMZN', 'AAPL', 'MSFT', 'NVDA', 'META', '^NDX']
#     startdate = '2018-12-31'
#     lastdate = '2023-12-31'
#     date = datetime.strptime(startdate, '%Y-%m-%d')
#     startdate = date - relativedelta(months=1)
#     startdate = startdate.strftime('%Y-%m-%d')
    
#     data = yf.download(tickers, start=startdate, end=lastdate, interval='1mo')['Adj Close']
#     monthly_prices = data.resample('M').last()
#     monthly_returns = monthly_prices.pct_change().dropna()  # Percentage change (returns)
    
#     benchmark_returns = monthly_returns["^NDX"]
#     stock_returns = monthly_returns[stock_ticker]
    
#     df = pd.DataFrame({
#         'Date': monthly_prices.index,
#         f'{stock_ticker} Adj Close': monthly_prices[stock_ticker],
#         'NDX Adj Close': monthly_prices['^NDX']
#     })
    
#     df[f'{stock_ticker}(Y)'] = stock_returns
#     df['NDX(X)'] = benchmark_returns
    
#     mean_y = df[f'{stock_ticker}(Y)'].mean()
#     mean_x = df['NDX(X)'].mean()
    
#     df[f'Y-Avg(Y)'] = df[f'{stock_ticker}(Y)'] - mean_y
#     df['X-Avg(X)'] = df['NDX(X)'] - mean_x
#     df['(X-Avg(X))*(Y-Avg(Y))'] = df['Y-Avg(Y)'] * df['X-Avg(X)']
#     df['power(X-Avg(X),2)'] = df['X-Avg(X)'] ** 2
#     df['power(Y-Avg(Y),2)'] = df['Y-Avg(Y)'] ** 2
#     df['NDX Adj Close - Avg(NDX)'] = df['NDX Adj Close'] - df['NDX Adj Close'].mean()
    
#     df = df.drop(df.index[0]).reset_index(drop=True)
    
#     correlation = df[f'{stock_ticker}(Y)'].corr(df['NDX(X)'])
    
#     sum_product = df['(X-Avg(X))*(Y-Avg(Y))'].sum()
#     sum_power_x = df['power(X-Avg(X),2)'].sum()
#     sum_power_y = df['power(Y-Avg(Y),2)'].sum()
#     sqrt_term = (sum_power_x * sum_power_y) ** 0.5
    
#     result = {
#         'Avg(X)': mean_x,
#         'Avg(Y)': mean_y,
#         'sum((X - Avg(X))*(Y - Avg(Y)))': sum_product,
#         'sum(power(X - Avg(X),2))': sum_power_x,
#         'sum(power(Y - Avg(Y),2))': sum_power_y,
#         'sqrt(sum(power(X - Avg(X),2)) * sum(power(Y - Avg(Y),2)))': sqrt_term,
#         'Correlation Coefficient': correlation
#     }
    
#     return result, df

# # Function to calculate 5Y Sharpe Ratio
# def calculate_5y_sharpe_ratio(ticker, monthly_returns, risk_free_rate=0.03):
#     returns = monthly_returns[ticker]
#     total_return = np.prod(1 + returns)  
#     M = len(returns)
#     annualized_return = ((total_return) ** (12 / M) - 1) * 100
    
#     std_monthly_return = returns.std()
#     annualized_std_dev = std_monthly_return * np.sqrt(12)
    
#     sharpe_ratio = ((annualized_return - risk_free_rate) / annualized_std_dev)
    
#     return annualized_return, annualized_std_dev, sharpe_ratio

# # Function to analyze Sharpe ratio for highest and lowest correlated stocks
# def sharpe_ratio_analysis(stocks, start_date, end_date):
#     tickers = stocks + ['^NDX']
#     date = datetime.strptime(start_date, '%Y-%m-%d')
#     start_date_adjusted = date - relativedelta(months=1)
#     start_date_adjusted = start_date_adjusted.strftime('%Y-%m-%d')

#     data = yf.download(tickers, start=start_date_adjusted, end=end_date, interval="1mo")['Adj Close']
#     data = data.dropna()
#     monthly_returns = data.pct_change().dropna()
    
#     correlations = monthly_returns.corr()['^NDX']
#     highest_corr_ticker = correlations.drop('^NDX').idxmax()
#     lowest_corr_ticker = correlations.drop('^NDX').idxmin()

#     results = []
#     for ticker in [highest_corr_ticker, lowest_corr_ticker]:
#         annualized_return, annualized_std_dev, sharpe_ratio = calculate_5y_sharpe_ratio(ticker, monthly_returns)
#         results.append({
#             "Ticker": ticker,
#             "5Y Annualized Return (%)": annualized_return,
#             "5Y Annualized Std Dev": annualized_std_dev,
#             "5Y Annualized Sharpe Ratio": sharpe_ratio,
#         })

#     results_df = pd.DataFrame(results)
    
#     return results_df

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         # Get form inputs
#         stocks = request.form['stocks'].split(',')
#         start_date = request.form['start_date']
#         end_date = request.form['end_date']
        
#         all_results = {}
#         all_dfs = {}

#         # Calculate correlations for each stock
#         for stock in stocks:
#             result, df = calculate_correlation(stock)
#             all_results[stock] = result
#             all_dfs[stock] = df

#         # Prepare the correlation table
#         final_df = pd.DataFrame(all_results)
#         correlation_table = final_df.to_html(classes='table table-bordered table-striped', index=True)

#         # Perform Sharpe ratio analysis
#         sharpe_results = sharpe_ratio_analysis(stocks, start_date, end_date)
#         sharpe_table = sharpe_results.to_html(classes='table table-bordered table-striped', index=False)

#         # Render results
#         return render_template('results.html', correlation_table=correlation_table, sharpe_table=sharpe_table)
    
#     return render_template('index.html')

# if __name__ == '__main__':
#     app.run(debug=True)


import yfinance as yf
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
import numpy as np
from flask import Flask, render_template, request

app = Flask(__name__)

# Function to calculate correlation
def calculate_correlation(stock_ticker, startdate, lastdate):
    tickers = ['AMZN', 'AAPL', 'MSFT', 'NVDA', 'META', '^NDX']
    date = datetime.strptime(startdate, '%Y-%m-%d')
    startdate = date - relativedelta(months=1)
    startdate = startdate.strftime('%Y-%m-%d')
    
    data = yf.download(tickers, start=startdate, end=lastdate, interval='1mo')['Adj Close']
    monthly_prices = data.resample('M').last()
    monthly_returns = monthly_prices.pct_change().dropna()  # Percentage change (returns)
    
    benchmark_returns = monthly_returns["^NDX"]
    stock_returns = monthly_returns[stock_ticker]
    
    df = pd.DataFrame({
        'Date': monthly_prices.index,
        f'{stock_ticker} Adj Close': monthly_prices[stock_ticker],
        'NDX Adj Close': monthly_prices['^NDX']
    })
    
    df[f'{stock_ticker}(Y)'] = stock_returns
    df['NDX(X)'] = benchmark_returns
    
    mean_y = df[f'{stock_ticker}(Y)'].mean()
    mean_x = df['NDX(X)'].mean()
    
    df[f'Y-Avg(Y)'] = df[f'{stock_ticker}(Y)'] - mean_y
    df['X-Avg(X)'] = df['NDX(X)'] - mean_x
    df['(X-Avg(X))*(Y-Avg(Y))'] = df['Y-Avg(Y)'] * df['X-Avg(X)']
    df['power(X-Avg(X),2)'] = df['X-Avg(X)'] ** 2
    df['power(Y-Avg(Y),2)'] = df['Y-Avg(Y)'] ** 2
    df['NDX Adj Close - Avg(NDX)'] = df['NDX Adj Close'] - df['NDX Adj Close'].mean()
    
    df = df.drop(df.index[0]).reset_index(drop=True)
    
    correlation = df[f'{stock_ticker}(Y)'].corr(df['NDX(X)'])
    
    sum_product = df['(X-Avg(X))*(Y-Avg(Y))'].sum()
    sum_power_x = df['power(X-Avg(X),2)'].sum()
    sum_power_y = df['power(Y-Avg(Y),2)'].sum()
    sqrt_term = (sum_power_x * sum_power_y) ** 0.5
    
    result = {
        'Avg(X)': mean_x,
        'Avg(Y)': mean_y,
        'sum((X - Avg(X))*(Y - Avg(Y)))': sum_product,
        'sum(power(X - Avg(X),2))': sum_power_x,
        'sum(power(Y - Avg(Y),2))': sum_power_y,
        'sqrt(sum(power(X - Avg(X),2)) * sum(power(Y - Avg(Y),2)))': sqrt_term,
        'Correlation Coefficient': correlation
    }
    
    return result, df

# Function to calculate 5Y Sharpe Ratio
def calculate_5y_sharpe_ratio(ticker, monthly_returns, risk_free_rate=0.03):
    returns = monthly_returns[ticker]
    total_return = np.prod(1 + returns)  
    M = len(returns)
    annualized_return = ((total_return) ** (12 / M) - 1) * 100
    
    std_monthly_return = returns.std()
    annualized_std_dev = std_monthly_return * np.sqrt(12)
    
    sharpe_ratio = ((annualized_return - risk_free_rate) / annualized_std_dev)
    
    return annualized_return, annualized_std_dev, sharpe_ratio

# Function to analyze Sharpe ratio for highest and lowest correlated stocks
def sharpe_ratio_analysis(stocks, start_date, end_date):
    tickers = stocks + ['^NDX']
    date = datetime.strptime(start_date, '%Y-%m-%d')
    start_date_adjusted = date - relativedelta(months=1)
    start_date_adjusted = start_date_adjusted.strftime('%Y-%m-%d')

    data = yf.download(tickers, start=start_date_adjusted, end=end_date, interval="1mo")['Adj Close']
    data = data.dropna()
    monthly_returns = data.pct_change().dropna()
    
    correlations = monthly_returns.corr()['^NDX']
    highest_corr_ticker = correlations.drop('^NDX').idxmax()
    lowest_corr_ticker = correlations.drop('^NDX').idxmin()

    results = []
    for ticker in [highest_corr_ticker, lowest_corr_ticker]:
        annualized_return, annualized_std_dev, sharpe_ratio = calculate_5y_sharpe_ratio(ticker, monthly_returns)
        results.append({
            "Ticker": ticker,
            "5Y Annualized Return (%)": annualized_return,
            "5Y Annualized Std Dev": annualized_std_dev,
            "5Y Annualized Sharpe Ratio": sharpe_ratio,
        })

    results_df = pd.DataFrame(results)
    
    return results_df

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get form inputs
        stocks = request.form['stocks'].split(',')
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        
        all_results = {}
        all_dfs = {}

        # Calculate correlations for each stock
        for stock in stocks:
            result, df = calculate_correlation(stock, start_date, end_date)
            all_results[stock] = result
            all_dfs[stock] = df

        # Prepare the correlation table
        final_df = pd.DataFrame(all_results)
        correlation_table = final_df.to_html(classes='table table-bordered table-striped', index=True)

        # Perform Sharpe ratio analysis
        sharpe_results = sharpe_ratio_analysis(stocks, start_date, end_date)
        sharpe_table = sharpe_results.to_html(classes='table table-bordered table-striped', index=False)

        # Render results
        return render_template('results.html', correlation_table=correlation_table, sharpe_table=sharpe_table)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
