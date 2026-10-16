import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

df=pd.read_csv("voltaje_distancia.csv")
# Si tienes una columna que identifica cada medición individual (ej: 'medicion' o 'indice')
df_pivoteado = df.pivot(index='distancia', columns='indice', values='voltaje')
df_pivoteado=df_pivoteado.reset_index()


def ley_de_potencia_normalizada(x,p):
    y=(40/x)**p #(x0/x)^p
    return y

x=df_pivoteado.distancia
exponente=[]
error=[]

for i in df_pivoteado.columns !="distancia":
    y=df_pivoteado[i]
    p, matriz_covarianza = curve_fit(ley_de_potencia_normalizada, x, y, p0=[100.0, -2.0])
    exponente.append(p)
    stdev=np.sqrt(np.diag(matriz_covarianza))
    error.append(stdev)

plt.figure(figsize=(8, 5))

# Usamos errorbar en lugar de scatter
plt.errorbar(
    x, y,
    yerr=error,     # Barras de error verticales
    fmt='o',          # Formato de los puntos (círculos)
    color='blue',     # Color de los puntos y barras
    ecolor='gray',    # Color de las líneas de error (un gris queda sutil y prolijo)
    elinewidth=1.5,   # Grosor de la barra de error
    capsize=3,        # Pequeñas "pestañas" en los extremos de las barras de error
    label='Datos experimentales con error'
)
plt.show()