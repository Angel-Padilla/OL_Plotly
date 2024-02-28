import xml.etree.ElementTree as XML
from dotenv import load_dotenv
from tools.XML.config_loader import *
from tools.CSV.csv_reader import *
import plotly.graph_objects as go 
import plotly.io as pio
from plot import *
import importlib
import argparse
import dotenv
import os

importlib.reload(dotenv)
load_dotenv()

class work:
    cleanup = None
    analysis = None
    graph:plot = plot()

def main():
    parser = argparse.ArgumentParser(description='plot CSVs using a configuration file.')
    parser.add_argument('directory',help='an integer for the accumulator')
    args = parser.parse_args()
    print("main")

#put in here what happens only when the script is executed directly, maybe never
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='plot CSVs using a configuration file.')
    parser.add_argument('directory',help='an integer for the accumulator')
    parser.add_argument('-s', '--show',action='store_true')
    args = parser.parse_args()
    
    #iterate over every file in the given directory, if is a CSV load into the plot and 
    #generate the graph

    filePath = os.path.join(args.directory,os.getenv("FILE_NAME"))
    separator = os.getenv("PATH_SEPARATOR")
    XML_CONFIG:XML.ElementTree =  parse_XML_config_file(filePath) #test
    _work:work = work()

    for file in os.scandir(args.directory):
        if file.is_file():
            fig = go.Figure()
            filename = file.path.split(separator)[-1]
            if filename.split(".")[-1].upper() != "CSV":
                continue
            filename = ".".join(filename.split(".")[:-1])
            _work.graph.clear_pĺot()
            load_config_from_XML(XML_CONFIG,_work.graph, filename)
            load_csv(file.path)
            _plot_config = _work.graph.get_plot_config()
            #iterate over the traces and load the data
            for _trace in _work.graph.traces:
                trace_config = _trace.get_trace_config()
                _trace.set_X_data(load_x_data(trace_config["over"]))
                _trace.set_Y_data(load_y_data(trace_config["name"]))
                _trace_line = go.scatter.Line(color=trace_config["color"])
                fig.add_trace(go.Scatter(x=_trace.Xdata,
                                         y=_trace.Ydata,
                                         name=trace_config["legend"],
                                         line=_trace_line,
                                         ))
            #set plot title
            figure_title = _plot_config["title"]
            fig.update_layout(title_text=figure_title)
            #set main axis labels
            fig.update_xaxes(title_text=_plot_config["xAxis"]["label"])
            fig.update_yaxes(title_text=_plot_config["yAxis"]["label"])

            #save html file
            pio.write_html(fig, file="{0}/{1}.html".format(args.directory,filename), auto_open=args.show)
    print("done")