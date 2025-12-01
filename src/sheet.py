import pandas as pd
from config import EXCEL_PATH

def loading_sheet():
    df = pd.read_excel(EXCEL_PATH)
    return df

def save_sheet(df):
    df.to_excel(EXCEL_PATH, index=False)

def get_pendings(df):
    return df[df["status"] == "pendente"]
