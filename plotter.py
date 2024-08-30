import xml.etree.ElementTree as XML
from dotenv import load_dotenv
from tools.XML.config_loader import *
from tools.CSV.csv_reader import *
import plotly.graph_objects as go 
import plotly.io as pio
from plot import *
import importlib
import threading
import argparse
import dotenv
import os
from enum import Enum


class THREAD_SLOT_STATUS(Enum):
    FREE = 0
    BUSY = 1
    ENDED = 2

MAX_THREADS = 6 
THREADING_ENABLED = False

threads_status_stack = [THREAD_SLOT_STATUS.FREE]*MAX_THREADS

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

def get_free_thread_slot(thread_status_stack:list[THREAD_SLOT_STATUS]):
    for index, slot_status in enumerate(thread_status_stack):
        status = "busy" if ( slot_status == THREAD_SLOT_STATUS.BUSY ) else ("free" if ( slot_status == THREAD_SLOT_STATUS.FREE ) else ("ended" if ( slot_status == THREAD_SLOT_STATUS.ENDED ) else "unknown" ))
        print("slot [ " + str(index) + " ] is :" + status )
        if slot_status == THREAD_SLOT_STATUS.FREE or slot_status == THREAD_SLOT_STATUS.ENDED:
            return index
    return -1

def generate_html_task(file,directory, show, thread_index):
    threads_status_stack[thread_index] = THREAD_SLOT_STATUS.BUSY
    generate_html_plot_from_file(file, directory, show);
    threads_status_stack[thread_index] = THREAD_SLOT_STATUS.ENDED


def generate_html_plot_from_file(file, directory, show):
    if file.is_file():
        fig = go.Figure()
        filename = file.path.split(separator)[-1]
        if filename.split(".")[-1].upper() != "CSV":
            return;
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
                                        xaxis="x2" if ( trace_config["reference"][0] == "aux" and _plot_config["xAxis"]["aux"]["enabled"] ) else "x",
                                        yaxis="y2" if ( trace_config["reference"][1] == "aux" and _plot_config["yAxis"]["aux"]["enabled"] ) else "y",
                                        ))
        #set plot title
        figure_title = _plot_config["title"]

        PLOT_LAYOUT_CONFIG:dict = {}
        PLOT_LAYOUT_CONFIG["title_text"] = figure_title

        #configure MAIN X AXIS
        MAIN_X_AXIS_CONFIG:dict = {}
        MAIN_X_AXIS_CONFIG["title_text"] = _plot_config["xAxis"]["label"]
        main_x_axis_autorange_type = get_autorange_type(_plot_config["xAxis"]["range"]) 
        if main_x_axis_autorange_type != False:
            MAIN_X_AXIS_CONFIG["autorange"] = main_x_axis_autorange_type
        if main_x_axis_autorange_type != True:
            MAIN_X_AXIS_CONFIG["range"] = [(int(bound) if bound != "auto" else None) for bound in _plot_config["xAxis"]["range"]]
        
        #configure MAIN Y AXIS
        MAIN_Y_AXIS_CONFIG:dict = {}
        MAIN_Y_AXIS_CONFIG["title_text"] = _plot_config["yAxis"]["label"]
        MAIN_X_AXIS_CONFIG["side"] = "left"
        main_y_axis_autorange_type = get_autorange_type(_plot_config["yAxis"]["range"]) 
        if main_y_axis_autorange_type != False:
            MAIN_Y_AXIS_CONFIG["autorange"] = main_y_axis_autorange_type
        if main_y_axis_autorange_type != True:
            MAIN_Y_AXIS_CONFIG["range"] = [(int(bound) if bound != "auto" else None) for bound in _plot_config["yAxis"]["range"]]

        #set main axis labels
        PLOT_LAYOUT_CONFIG["xaxis"] = MAIN_X_AXIS_CONFIG
        PLOT_LAYOUT_CONFIG["yaxis"] = MAIN_Y_AXIS_CONFIG

        #Configure AUX X AXIS
        if _plot_config["xAxis"]["aux"]["enabled"]:
            AUX_X_AXIS_CONFIG:dict = {}
            AUX_X_AXIS_CONFIG["side"] = "up"
            AUX_X_AXIS_CONFIG["title_text"] = _plot_config["xAxis"]["aux"]["label"]
            AUX_X_AXIS_CONFIG["overlaying"] = "x"
            AUX_X_AXIS_CONFIG["tickmode"] = "sync"
            aux_x_axis_autorange_type = get_autorange_type(_plot_config["xAxis"]["aux"]["range"]) 
            if aux_x_axis_autorange_type != False:
                AUX_X_AXIS_CONFIG["autorange"] = main_x_axis_autorange_type
            if main_x_axis_autorange_type != True:
                AUX_X_AXIS_CONFIG["range"] = [(int(bound) if bound != "auto" else None) for bound in _plot_config["xAxis"]["aux"]["range"]]

            PLOT_LAYOUT_CONFIG["xaxis2"] = AUX_X_AXIS_CONFIG


        #Configure AUX Y AXIS
        if _plot_config["yAxis"]["aux"]["enabled"]:
            AUX_Y_AXIS_CONFIG:dict = {}
            AUX_Y_AXIS_CONFIG["side"] = "right"
            AUX_Y_AXIS_CONFIG["title_text"] = _plot_config["yAxis"]["aux"]["label"]
            AUX_Y_AXIS_CONFIG["overlaying"] = "y"
            AUX_Y_AXIS_CONFIG["tickmode"] = "sync"
            aux_y_axis_autorange_type = get_autorange_type(_plot_config["yAxis"]["aux"]["range"]) 
            if aux_y_axis_autorange_type != False:
                AUX_Y_AXIS_CONFIG["autorange"] = aux_y_axis_autorange_type
            if aux_y_axis_autorange_type != True:
                AUX_Y_AXIS_CONFIG["range"] = [(int(bound) if bound != "auto" else None) for bound in _plot_config["yAxis"]["aux"]["range"]]

            PLOT_LAYOUT_CONFIG["yaxis2"] = AUX_Y_AXIS_CONFIG

        fig.update_layout(PLOT_LAYOUT_CONFIG)


        #save html file
        pio.write_html(fig, file="{0}/{1}.html".format(directory,filename), auto_open=show)


#put in here what happens only when the script is executed directly, maybe never
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='plot CSVs using a configuration file.')
    parser.add_argument('directory',help='an integer for the accumulator')
    parser.add_argument('-s', '--show',action='store_true')
    parser.add_argument('-t', '--threading',action='store_true', help='enable threading')
    args = parser.parse_args()
    
    #iterate over every file in the given directory, if is a CSV load into the plot and 
    #generate the graph

    filePath = os.path.join(args.directory,os.getenv("FILE_NAME"))
    separator = os.getenv("PATH_SEPARATOR")
    XML_CONFIG:XML.ElementTree =  parse_XML_config_file(filePath) #test
    _work:work = work()



    for file in os.scandir(args.directory):
        if args.threading :
            # wait for a thread slot to be free
            thread_index = get_free_thread_slot(threads_status_stack) 
            while thread_index == -1:
                thread_index = get_free_thread_slot(threads_status_stack)
                continue
            # add the new thread
            # threading.Thread(target=generate_html_plot_from_file, args=[file, args.directory, args.show])
            threading.Thread(target=generate_html_task, args=[file, args.directory, args.show, thread_index])
        else:    
            generate_html_plot_from_file(file=file, directory=args.directory, show=args.show)
        # if file.is_file():
        #     fig = go.Figure()
        #     filename = file.path.split(separator)[-1]
        #     if filename.split(".")[-1].upper() != "CSV":
        #         continue
        #     filename = ".".join(filename.split(".")[:-1])
        #     _work.graph.clear_pĺot()
        #     load_config_from_XML(XML_CONFIG,_work.graph, filename)
        #     load_csv(file.path)
        #     _plot_config = _work.graph.get_plot_config()
        #     #iterate over the traces and load the data
        #     for _trace in _work.graph.traces:
        #         trace_config = _trace.get_trace_config()
        #         _trace.set_X_data(load_x_data(trace_config["over"]))
        #         _trace.set_Y_data(load_y_data(trace_config["name"]))
        #         _trace_line = go.scatter.Line(color=trace_config["color"])
        #         fig.add_trace(go.Scatter(x=_trace.Xdata,
        #                                  y=_trace.Ydata,
        #                                  name=trace_config["legend"],
        #                                  line=_trace_line,
        #                                  xaxis="x2" if ( trace_config["reference"][0] == "aux" and _plot_config["xAxis"]["aux"]["enabled"] ) else "x",
        #                                  yaxis="y2" if ( trace_config["reference"][1] == "aux" and _plot_config["yAxis"]["aux"]["enabled"] ) else "y",
        #                                  ))
        #     #set plot title
        #     figure_title = _plot_config["title"]

        #     PLOT_LAYOUT_CONFIG:dict = {}
        #     PLOT_LAYOUT_CONFIG["title_text"] = figure_title

        #     #configure MAIN X AXIS
        #     MAIN_X_AXIS_CONFIG:dict = {}
        #     MAIN_X_AXIS_CONFIG["title_text"] = _plot_config["xAxis"]["label"]
        #     main_x_axis_autorange_type = get_autorange_type(_plot_config["xAxis"]["range"]) 
        #     if main_x_axis_autorange_type != False:
        #         MAIN_X_AXIS_CONFIG["autorange"] = main_x_axis_autorange_type
        #     if main_x_axis_autorange_type != True:
        #         MAIN_X_AXIS_CONFIG["range"] = [(int(bound) if bound != "auto" else None) for bound in _plot_config["xAxis"]["range"]]
            
        #     #configure MAIN Y AXIS
        #     MAIN_Y_AXIS_CONFIG:dict = {}
        #     MAIN_Y_AXIS_CONFIG["title_text"] = _plot_config["yAxis"]["label"]
        #     MAIN_X_AXIS_CONFIG["side"] = "left"
        #     main_y_axis_autorange_type = get_autorange_type(_plot_config["yAxis"]["range"]) 
        #     if main_y_axis_autorange_type != False:
        #         MAIN_Y_AXIS_CONFIG["autorange"] = main_y_axis_autorange_type
        #     if main_y_axis_autorange_type != True:
        #         MAIN_Y_AXIS_CONFIG["range"] = [(int(bound) if bound != "auto" else None) for bound in _plot_config["yAxis"]["range"]]

        #     #set main axis labels
        #     PLOT_LAYOUT_CONFIG["xaxis"] = MAIN_X_AXIS_CONFIG
        #     PLOT_LAYOUT_CONFIG["yaxis"] = MAIN_Y_AXIS_CONFIG

        #     #Configure AUX X AXIS
        #     if _plot_config["xAxis"]["aux"]["enabled"]:
        #         AUX_X_AXIS_CONFIG:dict = {}
        #         AUX_X_AXIS_CONFIG["side"] = "up"
        #         AUX_X_AXIS_CONFIG["title_text"] = _plot_config["xAxis"]["aux"]["label"]
        #         AUX_X_AXIS_CONFIG["overlaying"] = "x"
        #         AUX_X_AXIS_CONFIG["tickmode"] = "sync"
        #         aux_x_axis_autorange_type = get_autorange_type(_plot_config["xAxis"]["aux"]["range"]) 
        #         if aux_x_axis_autorange_type != False:
        #             AUX_X_AXIS_CONFIG["autorange"] = main_x_axis_autorange_type
        #         if main_x_axis_autorange_type != True:
        #             AUX_X_AXIS_CONFIG["range"] = [(int(bound) if bound != "auto" else None) for bound in _plot_config["xAxis"]["aux"]["range"]]

        #         PLOT_LAYOUT_CONFIG["xaxis2"] = AUX_X_AXIS_CONFIG


        #     #Configure AUX Y AXIS
        #     if _plot_config["yAxis"]["aux"]["enabled"]:
        #         AUX_Y_AXIS_CONFIG:dict = {}
        #         AUX_Y_AXIS_CONFIG["side"] = "right"
        #         AUX_Y_AXIS_CONFIG["title_text"] = _plot_config["yAxis"]["aux"]["label"]
        #         AUX_Y_AXIS_CONFIG["overlaying"] = "y"
        #         AUX_Y_AXIS_CONFIG["tickmode"] = "sync"
        #         aux_y_axis_autorange_type = get_autorange_type(_plot_config["yAxis"]["aux"]["range"]) 
        #         if aux_y_axis_autorange_type != False:
        #             AUX_Y_AXIS_CONFIG["autorange"] = aux_y_axis_autorange_type
        #         if aux_y_axis_autorange_type != True:
        #             AUX_Y_AXIS_CONFIG["range"] = [(int(bound) if bound != "auto" else None) for bound in _plot_config["yAxis"]["aux"]["range"]]

        #         PLOT_LAYOUT_CONFIG["yaxis2"] = AUX_Y_AXIS_CONFIG

        #     fig.update_layout(PLOT_LAYOUT_CONFIG)


        #     #save html file
        #     pio.write_html(fig, file="{0}/{1}.html".format(args.directory,filename), auto_open=args.show)
    print("done")