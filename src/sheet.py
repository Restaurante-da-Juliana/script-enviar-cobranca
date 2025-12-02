import pandas as pd
from config import EXCEL_PATH

def loading_sheet():
    df = pd.read_excel(EXCEL_PATH)
    return df
