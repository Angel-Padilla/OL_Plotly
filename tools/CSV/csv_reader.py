import pandas as pd

CSV_DF:pd.DataFrame = None

def load_csv(filePath:str) -> None:
    global CSV_DF
    CSV_DF = pd.read_csv(filePath)

def load_x_data(x_header:str) -> list[float]:
    if x_header in CSV_DF.columns:
        return CSV_DF[x_header].values.tolist()
    return []
    
def load_y_data(y_header:str) -> list[float]:
    if y_header in CSV_DF.columns:
        return CSV_DF[y_header].values.tolist()
    return []