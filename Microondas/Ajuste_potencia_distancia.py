import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

df=pd.read_csv("voltaje_distancia.csv")
# Si tienes una columna que identifica cada medición individual (ej: 'medicion' o 'indice')
df_pivoteado = df.pivot(index='distancia', columns='indice', values='voltaje')
df_pivoteado=df_pivoteado.reset_index()


def ley_de_potencia_normalizada(x,p):
    y=(x/40)**p #(x0/x)^p
    return y

x=df_pivoteado.distancia
exponente=[]
error=[]

for i in df_pivoteado.columns:
    if i != "distancia":
        y=df_pivoteado[i]/df_pivoteado[i].iloc[0]
        p, matriz_covarianza = curve_fit(ley_de_potencia_normalizada, x, y, p0=[-2.0])
        exponente.append(p[0])
        stdev=np.sqrt(np.diag(matriz_covarianza))
        error.append(stdev[0])

exponente_promedio=np.mean(exponente)
error_exponente=np.std(exponente,ddof=1)

# Usamos errorbar en lugar de scatter
def graficar_exponente():
    plt.figure(figsize=(8, 5))
    plt.errorbar(
        range(len(exponente)), exponente,
        yerr=error,     # Barras de error verticales
        fmt='o',          # Formato de los puntos (círculos)
        color='blue',     # Color de los puntos y barras
        ecolor='gray',    # Color de las líneas de error (un gris queda sutil y prolijo)
        elinewidth=1.5,   # Grosor de la barra de error
        capsize=3,        # Pequeñas "pestañas" en los extremos de las barras de error
        label='Datos experimentales con error'
    )
    plt.axhline(
        y=exponente_promedio,  # El valor promedio que calculaste antes
        color='red',  # Color de la línea (rojo destaca bien)
        linestyle='--',  # Línea punteada ('--') o continua ('-')
        linewidth=2,  # Grosor de la línea
        label=f'Promedio: {exponente_promedio:.2f}'  # Texto para la leyenda
    )

    plt.xlabel('Número de serie de medición')
    plt.ylabel('Exponente (p) optimizado')
    plt.legend()
    plt.grid(True)
    plt.show()

def graficar_decaimiento():
    plt.figure(figsize=(8,5))
    for i in df_pivoteado.columns:
        if i != "distancia":
            y_norm = df_pivoteado[i] / df_pivoteado[i].iloc[0]
            plt.plot(x/40, y_norm, marker='o', alpha=0.7, label=f'Serie {i}')
    plt.xlabel('Distancia')
    plt.ylabel('Voltaje Normalizado')
    plt.title('Curvas de decaimiento normalizadas')
    plt.legend()
    plt.grid(True)
    plt.show()

print(exponente_promedio,error_exponente)
graficar_exponente()