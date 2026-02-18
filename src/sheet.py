import pandas as pd
import os

def loading_sheet():
    df = pd.read_excel(os.getenv("EXCEL_URL"))
    return df
