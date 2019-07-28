! pip install pandas_datareader
! pip install plotly
! pip install xlrd
! pip install yfinance - -upgrade - -no - cache - dir
import datetime
import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import pandas_datareader.data as pdr
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

init_notebook_mode(connected=True)
% matplotlib inline


def get_stock(tickers, start_date, end_date):
    def data(ticker):
        return pdr.get_data_yahoo(ticker, start=start_date, end=end_date)

    data_set = map(data, tickers)
    return pd.concat(data_set, keys=tickers, names=["Ticker", "Date"])


portfolio_df = pd.read_excel("sp500.xlsx")
start_sp = datetime.datetime(2013, 1, 1)
end_sp = datetime.datetime(2018, 3, 9)
end_of_year = datetime.datetime(2017, 12, 29)
yf.pdr_override()
sp500 = pdr.get_data_yahoo("^GSPC", start_sp, end_sp)
sp_500_adj_close = sp500[["Adj Close"]].reset_index()
sp_500_adj_close_start = sp_500_adj_close[sp_500_adj_close["Date"] == end_of_year]
tickers = portfolio_df["Ticker"].unique()

all_data = get_stock(tickers, start_sp, end_sp)
adj_close = all_data[["Adj Close"]].reset_index()
adj_close_start = adj_close[adj_close["Date"] == end_of_year]
adj_close_latest = adj_close[adj_close["Date"] == end_sp]
adj_close_latest.set_index("Ticker", inplace=True)
portfolio_df.set_index(["Ticker"], inplace=True)
merge_folio = pd.merge(portfolio_df, adj_close_latest, left_index=True, right_index=True)
merge_folio["ticker return"] = merge_folio["Adj Close"] / merge_folio["Unit Cost"] - 1
merge_folio.reset_index(inplace=True)
merge_folio_sp = pd.merge(merge_folio, sp_500_adj_close, left_on="Acquisition Date", right_on="Date")
del merge_folio_sp["Date_y"]

merge_folio_sp.rename(columns={"Date_x": "Latest Date", "Adj Close_x": "Ticker Adj Close",
                               "Adj Close_y": "SP 500 Initial Close"}, inplace=True)
merge_folio_sp["Equiv SP Shares"] = merge_folio_sp["Cost Basis"] / merge_folio_sp["SP 500 Initial Close"]
merge_folio_sp_lat = pd.merge(merge_folio_sp, sp_500_adj_close, left_on="Latest Date", right_on="Date")
del merge_folio_sp_lat["Date"]

merge_folio_sp_lat.rename(columns={"Adj Close": "SP 500 Latest Close"}, inplace=True)
merge_folio_sp_lat["SP Return"] = merge_folio_sp_lat["SP 500 Latest Close"] / \
                                  merge_folio_sp_lat["SP 500 Initial Close"] - 1
merge_folio_sp_lat["Abs Return Compare"] = merge_folio_sp_lat["ticker return"] - \
                                           merge_folio_sp_lat["SP Return"]
merge_folio_sp_lat["Ticker Share Value"] = merge_folio_sp_lat["Quantity"] * \
                                           merge_folio_sp_lat["Ticker Adj Close"]
merge_folio_sp_lat["SP 500 Value"] = merge_folio_sp_lat["Equiv SP Shares"] * \
                                     merge_folio_sp_lat["SP 500 Latest Close"]
merge_folio_sp_lat["Abs Value Compare"] = merge_folio_sp_lat["Ticker Share Value"] - \
                                          merge_folio_sp_lat["SP 500 Value"]
merge_folio_sp_lat["Stock Gain / Loss"] = merge_folio_sp_lat["Ticker Share Value"] - \
                                          merge_folio_sp_lat["Cost Basis"]
merge_folio_sp_lat["SP 500 Gain / Loss"] = merge_folio_sp_lat["SP 500 Value"] - \
                                           merge_folio_sp_lat["Cost Basis"]

merge_folio_sp_lat_YTD = pd.merge(merge_folio_sp_lat, adj_close_start, on="Ticker")
del merge_folio_sp_lat_YTD["Date"]
merge_folio_sp_lat_YTD.rename(columns={"Adj Close": "Ticker Start Year Close"}, inplace=True)
merge_folio_sp_lat_YTD_sp = pd.merge(merge_folio_sp_lat_YTD,
                                     sp_500_adj_close_start,
                                     left_on="Start of Year", right_on="Date")
del merge_folio_sp_lat_YTD_sp["Date"]
merge_folio_sp_lat_YTD_sp.rename(columns={"Adj Close": "SP Start Year Close"}, inplace=True)
merge_folio_sp_lat_YTD_sp["Share YTD"] = merge_folio_sp_lat_YTD_sp["Ticker Adj Close"] / \
                                         merge_folio_sp_lat_YTD_sp["Ticker Start Year Close"] - 1
merge_folio_sp_lat_YTD_sp["SP 500 YTD"] = merge_folio_sp_lat_YTD_sp["SP 500 Latest Close"] / \
                                          merge_folio_sp_lat_YTD_sp["SP Start Year Close"] - 1
merge_folio_sp_lat_YTD_sp = merge_folio_sp_lat_YTD_sp.sort_values(by="Ticker", ascending=True)
merge_folio_sp_lat_YTD_sp["Cum Invst"] = merge_folio_sp_lat_YTD_sp["Cost Basis"].cumsum()
merge_folio_sp_lat_YTD_sp["Cum Ticker Returns"] = merge_folio_sp_lat_YTD_sp["Ticker Share Value"].cumsum()
merge_folio_sp_lat_YTD_sp["Cum SP Returns"] = merge_folio_sp_lat_YTD_sp["SP 500 Value"].cumsum()
merge_folio_sp_lat_YTD_sp["Cum Ticker ROI Mult"] = merge_folio_sp_lat_YTD_sp["Cum Ticker Returns"] / \
                                                   merge_folio_sp_lat_YTD_sp["Cum Invst"]

portfolio_df.reset_index(inplace=True)
adj_close_acq_date = pd.merge(adj_close, portfolio_df, on="Ticker")
del adj_close_acq_date["Quantity"]
del adj_close_acq_date["Unit Cost"]
del adj_close_acq_date["Cost Basis"]
del adj_close_acq_date["Start of Year"]
adj_close_acq_date.sort_values(by=["Ticker", "Acquisition Date", "Date"], ascending=[True, True, True], inplace=True)
adj_close_acq_date["Date Delta"] = adj_close_acq_date["Date"] - adj_close_acq_date["Acquisition Date"]
adj_close_acq_date["Date Delta"] = adj_close_acq_date[["Date Delta"]].apply(pd.to_numeric)
adj_close_acq_date_modified = adj_close_acq_date[adj_close_acq_date["Date Delta"] >= 0]

adj_close_pivot = adj_close_acq_date_modified.pivot_table(index=["Ticker", "Acquisition Date"], values="Adj Close",
                                                          aggfunc=np.max)
adj_close_pivot.reset_index(inplace=True)
adj_close_pivot_merge = pd.merge(adj_close_pivot, adj_close, on=["Ticker", "Adj Close"])
merge_folio_sp_lat_YTD_sp_close_high = pd.merge(merge_folio_sp_lat_YTD_sp,
                                       adj_close_pivot_merge,
                                       on=["Ticker", "Acquisition Date"])
merge_folio_sp_lat_YTD_sp_close_high.rename(columns={"Adj Close": "Closing High Adj Close",
                                                     "Date": "Closing High Adj Close Date"}, inplace=True)
merge_folio_sp_lat_YTD_sp_close_high["Pct off High"] = merge_folio_sp_lat_YTD_sp_close_high["Ticker Adj Close"] / \
                                                       merge_folio_sp_lat_YTD_sp_close_high["Closing High Adj Close"] - 1

trace_one = go.Bar(x=merge_folio_sp_lat_YTD_sp_close_high["Ticker"][0:10],
                   y=merge_folio_sp_lat_YTD_sp_close_high["Stock Gain / Loss"][0:10],
                   name="Ticker Total Return ($)")
trace_two = go.Bar(x=merge_folio_sp_lat_YTD_sp_close_high["Ticker"][0:10],
                   y=merge_folio_sp_lat_YTD_sp_close_high["SP 500 Gain / Loss"][0:10],
                   name="SP 500 Total Return ($)")
trace_three = go.Scatter(x=merge_folio_sp_lat_YTD_sp_close_high["Ticker"][0:10],
                         y=merge_folio_sp_lat_YTD_sp_close_high["ticker return"][0:10],
                         name="Ticker Total Return %", yaxis="y2")
data = [trace_one, trace_two, trace_three]
layout = go.Layout(title="Gain / Loss -- Total Return vs S&P 500",
                   barmode="group",
                   yaxis=dict(title="Gain / Loss ($)"),
                   yaxis2=dict(title="Ticker Return", overlaying="y",
                               side="right", tickformat=".2%"),
                   xaxis=dict(title="Ticker"),
                   legend=dict(x=.75, y=1))
fig = go.Figure(data=data, layout=layout)

iplot(fig)