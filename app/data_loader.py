import pandas as pd

def load_data():
    # Link do Google Sheets para download automático em formato Excel
    url = "https://docs.google.com/spreadsheets/d/1MoGJPvpWaelOXrF34uA88DCQqkcVADTW/export?format=xlsx"

    # STATUS DOBRADEIRA
    status_dobradeira = pd.read_excel(url, sheet_name=0, skiprows=7, nrows=11, usecols="A:C")
    status_dobradeira.columns = status_dobradeira.iloc[0]
    status_dobradeira = status_dobradeira[1:].reset_index(drop=True)

    # PEÇAS FALTANTES
    pecas_faltantes_solda = pd.read_excel(url, sheet_name=0, skiprows=20, nrows=11, usecols="A:E")
    pecas_faltantes_solda.columns = pecas_faltantes_solda.iloc[0]
    pecas_faltantes_solda = pecas_faltantes_solda[1:].reset_index(drop=True)

    # ESTOQUE INTERMEDIÁRIO
    estoque_intermediario = pd.read_excel(url, sheet_name=0, skiprows=32, nrows=11, usecols="A:E")
    estoque_intermediario.columns = estoque_intermediario.iloc[0]
    estoque_intermediario = estoque_intermediario[1:].reset_index(drop=True)

    return status_dobradeira, pecas_faltantes_solda, estoque_intermediario
