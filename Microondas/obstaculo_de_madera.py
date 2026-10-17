import pandas as pd
import matplotlib.pyplot as plt

df=pd.read_csv("obstaculo_de_madera.csv")
df_pivoteado=df.pivot(index="distancia",columns="indice",values="voltaje")
df_pivoteado.reset_index(inplace=True)

#la medicion se hizo en inches así que lo paso a cm
df_pivoteado.distancia=df_pivoteado.distancia*2.54

def graficar_voltaje_distancia():
    x=df_pivoteado.distancia
    plt.figure(figsize=(8,5))
    for i in df_pivoteado.columns:
        if i != "distancia":
            y=df_pivoteado[i]
            plt.plot(x,y)
    plt.grid(True)
    plt.show()
print(df_pivoteado)
graficar_voltaje_distancia()