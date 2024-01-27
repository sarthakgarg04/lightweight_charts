import pandas as pd
import pandas_ta as ta
import yfinance as yf
from lightweight_charts import Chart
import datetime as dt
import pandas_datareader.data as pdr

yf.pdr_override()
end = dt.datetime.now()

candle_count={
    
    '1mo':10000,
    '1wk':10000,
    "1d":10000,
    "1h":729,
    "15m":59,
    "5m":59,
    "1m":6
}

def get_bar_data(symbol,timeframe):

    start=end - dt.timedelta(days=candle_count[timeframe])
    df=pdr.get_data_yahoo(symbol, start, end, interval=timeframe)
    df = df.reset_index()
    df.columns = df.columns.str.lower()
    if df.columns[0]=="datetime":
        df.rename(columns={"datetime":"date"}, inplace=True)
    df=df.dropna()
    return(df)


def on_search(chart, searched_string):  # Called when the user searches.
    new_data = get_bar_data(searched_string, chart.topbar['timeframe'].value)
    if new_data.empty:
        return
    chart.topbar['symbol'].set(searched_string)
    chart.set(new_data)


def on_timeframe_selection(chart):  # Called when the user changes the timeframe.
    new_data = get_bar_data(chart.topbar['symbol'].value, chart.topbar['timeframe'].value)
    if new_data.empty:
        return
    chart.set(new_data, True)

def menu_options(chart):

    if chart.topbar['menu'].value == "sma10":
        x=10
    elif chart.topbar['menu'].value == "sma20":
        x=20
    else: x=50

    new_data = get_bar_data(chart.topbar['symbol'].value, chart.topbar['timeframe'].value)
    new_data["sma"]= ta.sma(new_data["close"] , length=x)
    columns=["date","sma"]
    sma_data = new_data[columns].dropna().copy()  # Make a copy of the data
    sma_data.rename(columns={ "sma": "value"}, inplace=True) 
    line = chart.create_line()    
    line.set(sma_data)




def on_horizontal_line_move(chart, line):
    print(f'Horizontal line moved to: {line.price}')



# if __name__ == '__main__':

def tvchart():
    chart = Chart(toolbox=True)
    chart.legend(True)

    chart.events.search += on_search

    chart.topbar.textbox('symbol', 'RELIANCE.NS')
    chart.topbar.switcher('timeframe', ('1m', '5m', '15m', '1h', '1d', '1wk', '1mo'), default='1d',
                          func=on_timeframe_selection)
    chart.topbar.menu('menu',('sma10','sma20','sma50'),func=menu_options)
    df = get_bar_data('RELIANCE.NS', '1d')
    print(df)
    chart.set(df)

    chart.horizontal_line(200, func=on_horizontal_line_move)

    # chart.show(block=True)
    return chart

if __name__ == "__main__":

    print(tvchart().show(block=True))