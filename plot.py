from tools.configurations.config import Marker, Axis
from xml.etree.ElementTree import Element

DEFAULT_TRACE_CONFIG:dict = {
    "name":"header name",
    "over":"header name",
    "type":"line",
    "style":"solid",
    "color": "#000000",
    "marker": Marker.CIRCLE,
    "width": 1,
    "legend": "generic legend",
    "reference": [Axis.XMAIN, Axis.YMAIN],
}

DEFAULT_PLOT_CONFIG:dict = {
    "file":"global",
    "title":"plot",
    "xAxis":{
            "label": "X Axis",
            "range":[None, None],
            "aux":
                {
                    "active": False,
                    "label": "X Axis 2",
                    "range":[None, None],
                }
            },
    "yAxis":{
            "label": "Y Axis",
            "range":[None, None],
            "aux":
                {
                    "active": False,
                    "label": "Y Axis 2",
                    "range":[None, None],
                }
            }
}

class trace:
    def __init__(self):
        self.Xdata:list[float] = None
        self.Ydata:list[float] = None
        self.__meta:dict = dict.copy(DEFAULT_TRACE_CONFIG)

    def pair_data(self):
        """
        If the data X and Y have different dimensions fill the shortest with 0's
        """

        if(self.Xdata.__len__() < self.Ydata.__len__()):
            while len(self.Xdata) < len(self.Ydata):
                self.Xdata.append(0)
        else:
            while len(self.Xdata) < len(self.Ydata):
                self.Ydata.append(0)


    def set_X_data(self,xData:list[float])->None:
        if xData.__len__() < 1:
            self.Xdata = None
        self.Xdata = xData

        #if Y data was already set 
        if self.Ydata != None:
            self.pair_data()

    def set_Y_data(self,yData:list[float])->None:
        if yData.__len__() < 1:
            self.Xdata = None
        self.Ydata = yData

        #if X data was already set 
        if self.Xdata != None:
            self.pair_data()
    
    def set_trace_config(self,**kwargs)->None:
        """
        Set the configuration of the trace to be ploted
        """
        for key, value in kwargs.items():
            if key in self.__meta.keys():
                self.__meta[key] = value
            else:
                print(f"element {key} not found in trace.__meta")
    
    def get_trace_config(self)->dict:
        """
        Get the configuration of the trace to be ploted
        """
        return self.__meta


            
class plot:
    
    def __init__(self) -> None:
        self.__meta:dict = dict.copy(DEFAULT_PLOT_CONFIG)
        self.traces:list[trace] = None

    def add_trace(self,**kwargs) ->None:
        new_trace:trace = trace()
        new_trace.set_trace_config(**kwargs)
        if self.traces == None:
            self.traces = []
        self.traces.append(new_trace)

    def clear_pĺot(self) -> None:
        self.traces = []

    def set_plot_config(self, **kwargs)->None:
        """
        Set the configuration of the trace to be ploted
        """
        for key, value in kwargs.items():
            if key in self.__meta.keys():
                self.__meta[key] = value
            else:
                print(f"element {key} not found in plot.__meta")

    def get_plot_config(self)->dict:
        """
        Get the configuration of the trace to be ploted
        """
        return self.__meta