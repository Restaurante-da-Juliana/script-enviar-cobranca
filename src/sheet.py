import pandas as pd
from config import EXCEL_URL

def loading_sheet():
    df = pd.read_excel(EXCEL_URL)
    return df
