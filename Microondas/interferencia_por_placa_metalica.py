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
    dataframe.reset_index(inplace=True)

#modifico los voltajes de df1574 porque están en volts y no en milivolts como el resto
dfs_pivoteados["df1574"].voltaje=dfs_pivoteados["df1574"].voltaje*1000

def grafica_distancia_voltaje():
    print(dfs_pivoteados.keys())
    nombre=input("elija que que grafica quiere:")
    x=dfs_pivoteados.distancia
    plt.figure(figsize=(8,5))
    if nombre in dfs_pivoteados.keys():
        y=dfs_pivoteados[nombre]
        plt.plot(x,y)
        plt.grid(True)
        plt.show()

grafica_distancia_voltaje()

