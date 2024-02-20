from dataclasses import dataclass
from enum import Enum, auto

class Axis(Enum):
    XAXIS = auto()
    XAXISAUX = auto()
    YAXIS = auto()
    YAXISAUX = auto()

@dataclass
class traceConfig:
    """
    Holds the config for the trace to be drawn
    """
    trace_type: int = 0
    line_color: int = 0x000000
    marker_type: int = 0
    width: int = 1
    legend: str = "traceX"
    references: list[Axis] = [Axis.XAXIS, Axis.YAXIS]

    def set_trace_type(self, type:int):
        self.trace_type = type

    def set_color(self, color:int):
        self.color = color

    def set_marker(self, marker:int):
        self.marker_type = marker

    def set_width(self, width:int):
        self.width = width

    def set_legend(self, legend:str):
        self.legend = legend

    def set_references(self, references:list[Axis]):
        if references[0] in [Axis.XAXIS, Axis.XAXISAUX] and references[1] in [Axis.YAXIS, Axis.YAXISAUX]:
            self.references = references

@dataclass
class plotConfig:
    """
    Holds the config for the plot to be drawn
    """
    title: str = "plot"
    xAxis: dict = {
        "label": "X Axis",
        "range":[None,None], 
        "aux":
            {
                "active": False,
                "label": "X Axis 2",
                "range":[None,None],
            }
    }
    yAxis: dict = {
        "label": "Y Axis",
        "range":[None,None],
        "aux":
            {
                "active": False,
                "label": "Y Axis 2",
                "range":[None,None],
            }
    }

    def get_plot_title(self):
        return self.title
   
    def set_plot_title(self, title:str):
        self.title = title
    
    def get_axis_conf(self):
        return [self.xAxis, self.yAxis]
    
    def set_label(self, axis:Axis , label:str):
        match(axis):
            case Axis.XAXIS:
                self.xAxis["label"] = label
            case Axis.XAXISAUX:
                self.xAxis["aux"]["label"] = label
            case Axis.YAXIS:
                self.yAxis["label"] = label
            case Axis.YAXISAUX:
                self.yAxis["aux"]["label"] = label
    
    def set_range(self, axis:Axis, range:list[float]):
        new_range = range
        if new_range.__len__ != 2:
            new_range = [None,None] #set automatic range if not well defined

        match(axis):
            case Axis.XAXIS:
                self.xAxis["range"] = new_range
            case Axis.XAXISAUX:
                self.xAxis["aux"]["range"] = new_range
            case Axis.YAXIS:
                self.yAxis["range"] = new_range
            case Axis.YAXISAUX:
                self.yAxis["aux"]["range"] = new_range
    
    def enable_second_axis(self, axis:Axis, enable:bool):
        match(axis):
            case Axis.XAXIS:
                self.xAxis["aux"]["active"] = enable
            case Axis.YAXIS:
                self.yAxis["aux"]["active"] = enable
            case _:
                self.xAxis["aux"]["active"] = False
                self.yAxis["aux"]["active"] = False