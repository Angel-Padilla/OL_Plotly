# OL_plotly

Repo intended for plotting .csv data offline using Plotly API

## Plot configuration data

Data on how will plotly plot the data will be provided on a '.pConf' file
it could be present on the folder the data to be plot is, or be provided
using CL arguments

## Plots

The plots (html files) are saved in the directory specified on the .pConf file
under the subdirectory named as the data itself, and under the folder named "plot"
The data used to plot the graph is moved to a "data" folder within the parent directory
of "plot" folder and renamed to "data"

All this mess will help its implementation on a server and keep everything organized