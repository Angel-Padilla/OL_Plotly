import xml.etree.ElementTree as XML
from plot import *
import os

def parse_XML_config_file(path:str) -> XML.ElementTree:
    return XML.parse(path).getroot().__copy__()

def load_config_from_XML(ROOT:XML.ElementTree, obj:plot, file:str = "global") ->None:
    """load config data from parsed XML file"""
    PLOT_CONFIG = None
    filename = file

    for _file in ROOT.find("plot").findall("file"):
        if _file.get("name") == file:
            PLOT_CONFIG = _file
            break

    if PLOT_CONFIG == None:
        PLOT_CONFIG = ROOT.find("plot").find("global")
        filename = "global-override" if PLOT_CONFIG.find("title").get("override").capitalize() == "True" else file
    #Create the dict holding the data to be set to the plot
    config:dict = {
        "file": filename,
        "title": PLOT_CONFIG.findtext("title"),
        "xAxis": {
                "label": PLOT_CONFIG.find("Axis").find("x").findtext("label"),
                "range": [bound for bound in PLOT_CONFIG.find("Axis").find("x").find("range").attrib.values()],
                "aux":
                    {
                        "active": PLOT_CONFIG.find("Axis").find("x").find("auxAxis").get("active").capitalize() == "True",
                        "label": PLOT_CONFIG.find("Axis").find("x").find("auxAxis").findtext("label"),
                        "range":[bound for bound in PLOT_CONFIG.find("Axis").find("x").find("auxAxis").find("range").attrib.values()],
                    }
                },
        "yAxis": {
                "label": PLOT_CONFIG.find("Axis").find("y").findtext("label"),
                "range": [bound for bound in PLOT_CONFIG.find("Axis").find("y").find("range").attrib.values()],
                "aux":
                    {
                        "active": PLOT_CONFIG.find("Axis").find("y").find("auxAxis").get("active").capitalize() == "True",
                        "label": PLOT_CONFIG.find("Axis").find("y").find("auxAxis").findtext("label"),
                        "range":[bound for bound in PLOT_CONFIG.find("Axis").find("y").find("auxAxis").find("range").attrib.values()],
                    }
                }
    }
    obj.set_plot_config(**config)
    
    #create the traces that will be plotted and configure them, no numeric data yet
    for _trace in PLOT_CONFIG.findall("trace"):
        t_config:dict = {
            "name":_trace.get("name"),
            "over":_trace.get("over"),
            "type": _trace.get("type"),
            "style": _trace.findtext("style"),
            "color": _trace.findtext("color"),
            "marker": _trace.findtext("marker"),
            "width": _trace.findtext("width"),
            "legend": _trace.findtext("legend"),
            "reference": [bound for bound in _trace.find("reference").attrib.values()],
        }
        obj.add_trace(**t_config)

    return