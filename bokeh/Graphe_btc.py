## simple_bokeh_dashboard.py
import bokeh
from bokeh.models import ColumnDataSource, HoverTool, Circle
from bokeh.io import curdoc
from bokeh.plotting import figure
from statistics import mean

import requests
import time
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

from bokeh.palettes import Category20
import random

data_source = ColumnDataSource(data = { "DateTime": [],"Close": [], "Volume": []
     #,"MA5": [], "MA10": [], "MA30": [], "MA60": []
     }) ## Data Source


df = pd.read_csv(r'./data_btcusdtshell.txt', header=None, names=['DateTime', 'Close', 'Volume'], sep="," )



df_filtre = df.tail(500)
#df_filtre = df[df['DateTime'] >= '2024-02-27 21:30:24.407012']

datetime_list = df_filtre['DateTime'].tolist()
close_list = df_filtre['Close'].tolist()
volume_list = df_filtre['Volume'].tolist()

#datetime_list = df['DateTime'].tolist()
#close_list = df['Close'].tolist()
#volume_list = df['Volume'].tolist()



for i in range(len(datetime_list)):
    new_data = {'DateTime': [datetime.strptime(datetime_list[i], '%Y-%m-%d %H:%M:%S.%f')], 'Close': [close_list[i]], 'Volume': [volume_list[i]]}
    data_source.stream(new_data)
    if i==(len(datetime_list)-1):
        print(new_data)


## Create Line Chart
fig = figure(x_axis_type="datetime",
             width=950, height=450,
             #tooltips=[("Close", "@Close{0.00} USD"), ("Time", "@Datetime{%Y-%m-%d %H:%M:%S}")],
             title = "Bitcoin Close Price Live (Every Second)")

line = fig.line(x="DateTime", y="Close", line_color="tomato", line_width=3.0, source=data_source)
line.glyph.line_color = "green"


#fig.line(x="Datetime", y="MA5", line_width=3.0, line_color="green", source=data_source)
#fig.line(x="Datetime", y="MA10", line_width=3.0, line_color="yellow", source=data_source)
#fig.line(x="Datetime", y="MA30", line_width=3.0, line_color="purple", source=data_source)
#fig.line(x="Datetime", y="MA60", line_width=3.0, line_color="orange", source=data_source)

fig.xaxis.axis_label="Date"
fig.yaxis.axis_label="Price ($)"


hover = HoverTool(renderers=[line],
                  tooltips=[("Close Price", "@Close{0.00} USD"), ("Time", "@DateTime{%Y-%m-%d %H:%M:%S}")],
                  formatters={"@DateTime": "datetime"})
fig.add_tools(hover)



# Créez un deuxième graphique pour afficher le volume
volume_fig = figure(x_axis_type="datetime",
                    width=950, height=300,
                    title="Bitcoin Volume Live (Every Second)")

volume_line = volume_fig.line(x="DateTime", y="Volume", line_color="blue", line_width=2.0, source=data_source)

volume_fig.xaxis.axis_label = "Date"
volume_fig.yaxis.axis_label = "Volume"

volume_hover = HoverTool(renderers=[volume_line],
                         tooltips=[("Volume", "@Volume{0.00} BTC"), ("Time", "@DateTime{%Y-%m-%d %H:%M:%S}")],
                         formatters={"@DateTime": "datetime"})
volume_fig.add_tools(volume_hover)



def update_chart():
    resp = requests.get("https://contract.mexc.com/api/v1/contract/kline/BTC_USDT")
    data = resp.json()
    #print("CLOSE: ",data['data']['close'][-1]," === VOLUME: ",data['data']['vol'][-1]," === DATE: ",datetime.now())
    new_row = {"DateTime": [datetime.now() + timedelta(milliseconds=41000)],"Close": [data['data']['close'][-1]],"Volume":[data['data']['vol'][-1]]}
    data_source.stream(new_row)
    print("NEW_ROW ++++++++",new_row)





curdoc().add_periodic_callback(update_chart, 30)

curdoc().add_root(fig)

curdoc().add_root(volume_fig)


