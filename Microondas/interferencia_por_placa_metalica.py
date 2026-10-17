import pandas as pd
import matplotlib.pyplot as plt

# 1. Las claves van como strings ("df6", etc.) y los valores son los nombres de los archivos
archivos = {
    "df6": "reflexion_metal_6cm.csv",
    "df9": "reflexion_metal_9cm.csv",
    "df1571": "reflexion_metal_15.2cm_71cm.csv",
    "df1574": "reflexion_metal_15.2cm_74cm.csv"
}

# 2. Creamos un diccionario vacío para guardar los DataFrames ya cargados
dfs = {}

# 3. Recorremos correctamente separando la clave (nombre) y el valor (archivo)
for nombre, archivo in archivos.items():
    dfs[nombre] = pd.read_csv(archivo)

dfs_pivoteados={}

for nombre,dataframe in dfs.items():
    dfs_pivoteados[nombre]=dataframe.pivot(index="distancia",columns="indice",values="voltaje")
    dataframe.reset_index()