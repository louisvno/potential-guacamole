from tkinter import *
import pandas_datareader as data
import pandas as pd
import talib
import numpy
from datetime import date
import fetch_stock_data as fsd
import plotly.express as px

def loadData():
    global graph

    today = date.today().isoformat()
    ticker = ticker_input.get()
    next_tick = float(next_tick_input.get())

    for interval, config in intervals_to_display.items():
        rsiData = calculateRsi(config["start_date"], today, ticker, interval, next_tick)
        graph[ticker + interval] = createGraph(rsiData, ticker)

        showGraph(graph[ticker + interval], config["frame"])

def calculateRsi(start_date, end_date, ticker, time_interval, next_tick):
    global ticker_data

    ticker_key = ticker + time_interval

    if ticker_key in ticker_data:
        df = ticker_data[ticker + time_interval]
    else :
        print("data fetched")
        df = fsd.fetch_stock_data(start_date, end_date, ticker, time_interval)
        ticker_data[ticker  + time_interval] = df
    
    return talib.RSI(numpy.append(df['Close'].values, next_tick))

def createGraph(rsiData, ticker) :
    fig = px.line(pd.DataFrame(rsiData), y=0, title=ticker, height=300)
    fig.update_layout( margin=dict(
        l=10,
        r=40,
        b=10,
        t=10,
        pad=0
    ))
    fig.update_yaxes(range=[0, 100])
    fig.add_hline(y=40, line_color='green')
    fig.add_hline(y=80, line_color='green', opacity=0.5)
    fig.add_hline(y=60, line_color='red')
    img_bytes = fig.to_image(format="png")

    return PhotoImage(data=img_bytes, format="png")

def showGraph(graph, frame):
    Label(frame, image=graph).grid(row=2, column=0, padx=5, pady=5)

root = Tk()
root.geometry('1900x1080')

graph = dict()
ticker_data = dict()

main_frame = Frame(root, width=600, height=400)
main_frame.grid(row=0)
Scrollbar(main_frame, orient="vertical")

input_frame = Frame(main_frame, width=200, height=400)
input_frame.grid(row=0, column=0, padx=10, pady=5)

graph_frame = Frame(main_frame, width=200, height=400)
graph_frame.grid(row=1, column=0, padx=10, pady=5)

hourly_graph_frame = Frame(main_frame, width=200, height=400)
hourly_graph_frame.grid(row=2, column=0, padx=10, pady=5)

daily_graph_frame = Frame(main_frame, width=200, height=400)
daily_graph_frame.grid(row=1, column=1, padx=10, pady=5)

weekly_graph_frame = Frame(main_frame, width=200, height=400)
weekly_graph_frame.grid(row=2, column=1, padx=10, pady=5)

Label(input_frame, text="Ticker").grid(row=0, column=0, padx=5)
ticker_input = Entry(input_frame, width = 10)
ticker_input.grid(row=0, column=1, pady= 5)

Label(input_frame, text="Next tick $").grid(row=1, column=0, padx=5)
next_tick_input = Entry(input_frame, width = 10)
next_tick_input.grid(row=1, column=1, pady= 5)

intervals_to_display = {
    '30m': {
        'start_date' : '2024-05-04',
        'frame' : graph_frame
    },
    '1h' : {
        'start_date' : '2024-05-04',
        'frame' : hourly_graph_frame
    },
    '1d': {
        'start_date' : '2023-01-01',
        'frame' : daily_graph_frame
    },
    '1wk': {
        'start_date' : '2022-01-01',
        'frame' : weekly_graph_frame
    }
}

run_button = Button(input_frame, text="Run", command=loadData).grid(row=9,column=0)

root.mainloop()

