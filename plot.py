from tools.configurations.config import *

class trace:
    Xdata:list[tuple[float]] = None
    Ydata:list[tuple[float]] = None
    meta:traceConfig = traceConfig()

    def pair_data(self):
        """
        If the data X and Y have different dimensions fill the shortest with 0's
        """

        if(self.Xdata.__len__() < self.Ydata.__len__()):
            tuple_size = len(self.Xdata[0])
            while len(self.Xdata) < len(self.Ydata):
                self.Xdata.append(tuple([0 for _ in range(0,tuple_size)]))
        else:
            tuple_size = len(self.Ydata[0])
            while len(self.Xdata) < len(self.Ydata):
                self.Ydata.append(tuple([0 for _ in range(0,tuple_size)]))


    def set_X_data(self,xData:list[tuple[float]])->None:
        if xData.__len__() < 1:
            self.Xdata = None
        self.Xdata = xData

        #if Y data was already set 
        if self.Ydata != None:
            self.pair_data()

    def set_Y_data(self,yData:list[tuple[float]])->None:
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
            if hasattr(self.meta, key):
                self.meta.__setattr__(key, value)
            else:
                print(f"attribute {key} not found in traceConfig")
            
class plot:
    meta:plotConfig = plotConfig()
    traces:list[trace] = None
    
    def __init__(self) -> None:
        pass

    def add_trace(self, xData:list[tuple[float]], yData:list[tuple[float]], **kwargs) ->None:
        new_trace:trace = trace()
        new_trace.set_trace_config(kwargs=kwargs)
        new_trace.set_X_data(xData=xData)
        new_trace.set_Y_data(yData=yData)

    def clear_pĺot(self) -> None:
        self.traces.clear()
    
    def set_plot_config(self, **kwargs)->None:
        """
        Set the configuration of the trace to be ploted
        """
        for key, value in kwargs.items():
            if hasattr(self.meta, key):
                self.meta.__setattr__(key, value)
            else:
                print(f"attribute {key} not found in traceConfig")