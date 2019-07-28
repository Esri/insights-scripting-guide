import numpy as np
import pandas as pd


def low_spread(stock_hist, price_type, num_spread=5):
    """ Get the lowest historical price for input spread of records."""
    return stock_hist.sort_values(by=[price_type]).head(num_spread)


def high_spread(stock_hist, price_type, num_spread=5):
    """ Get the lowest historical price for input spread of records."""
    return stock_hist.sort_values(by=[price_type]).tail(num_spread).sort_values(by=[price_type], ascending=False)


def adj_close_above_target(stock_hist, target_price, adj_close_column):
    """ Get the above target records for input target adjusted close price."""
    if isinstance(adj_close_column, int):
        adj_close_column = stock_hist.dtypes.index[adj_close_column]
    above_trg = stock_hist.loc[stock_hist[adj_close_column] > target_price]
    above_target = above_trg.sort_values(by=[adj_close_column], ascending=False)
    return above_target


def monthly_aggregate(stock_hist, adj_close_column, date_column):
    """ Get the monthly aggregate records for adjusted close price."""
    if isinstance(adj_close_column, int):
        adj_close_column = stock_hist.dtypes.index[adj_close_column]
    if isinstance(date_column, int):
        date_column = stock_hist.dtypes.index[date_column]
    date_split = stock_hist[[adj_close_column, date_column]].copy()
    date_split.insert(1, "year", pd.DatetimeIndex(date_split[date_column]).year)
    date_split.insert(2, "month", pd.DatetimeIndex(date_split[date_column]).month)
    index_set = date_split.set_index(["year", "month"])
    year_month_group = index_set.groupby(level=["year", "month"])
    return year_month_group.agg([np.mean, np.std, np.min, np.max])


def simple_daily_perc_change(stock_hist, adj_close_column, date_column):
    """ Get the simple daily percent change records for adjusted close price."""
    if isinstance(adj_close_column, int):
        adj_close_column = stock_hist.dtypes.index[adj_close_column]
    if isinstance(date_column, int):
        date_column = stock_hist.dtypes.index[date_column]
    per_change = stock_hist.set_index([date_column])
    per_change["daily_perc"] = (per_change[adj_close_column].pct_change() * 100).round(2)
    per_change.fillna(0, inplace=True)
    return per_change.loc[:, [adj_close_column, "daily_perc"]]


# Open AAPL stock historical data
aapl_hist = pd.read_csv("AAPL.csv")
# Set dataframe index
aapl_hist.set_index("trade_date")
# Set price column
price_type = "adj_close_price"

ten_low = low_spread(aapl_hist, price_type, num_spread=10)

ten_high = high_spread(aapl_hist, price_type, num_spread=10)

adj_above = adj_close_above_target(aapl_hist, 185, "adj_close_price")

month_agg = monthly_aggregate(aapl_hist, "adj_close_price", "trade_date")

daily_perc_delta = simple_daily_perc_change(aapl_hist, "adj_close_price", "trade_date")

aapl_hist['trade_date'] = pd.to_datetime(aapl_hist["trade_date"])

start_date = "2013-01-01"

end_date = "2013-08-01"

mask = (aapl_hist["trade_date"] > start_date) & (aapl_hist["trade_date"] <= end_date)

aapl_hist.loc[mask]

aapl_hist

%insights_return(appl_hist)
