import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

df = pd.read_csv("voltaje_distancia.csv")
df_pivoteado = df.pivot(index='distancia', columns='indice', values='voltaje')
df_pivoteado = df_pivoteado.reset_index()


def ley_de_potencia_normalizada(x, p):
    y = (x / 40) ** p  # (x/x0)^p
    return y


x = df_pivoteado.distancia
exponente = []
error = []

for i in df_pivoteado.columns:
    if i != "distancia":
        y = df_pivoteado[i] / df_pivoteado[i].iloc[0]
        p, matriz_covarianza = curve_fit(ley_de_potencia_normalizada, x, y, p0=[-2.0])
        exponente.append(p[0])
        stdev = np.sqrt(np.diag(matriz_covarianza))
        error.append(stdev[0])

exponente_promedio = np.mean(exponente)
error_exponente = np.std(exponente, ddof=1)

# Configuración general de tamaño de letra para los gráficos
plt.rcParams.update({'font.size': 12})


def graficar_exponente():
    plt.figure(figsize=(9, 5))
    plt.errorbar(
        range(len(exponente)), exponente,
        yerr=error,
        fmt='o',
        color='blue',
        ecolor='gray',
        elinewidth=1.5,
        capsize=3,
        label='Exponentes por serie'
    )
    plt.axhline(
        y=exponente_promedio,
        color='red',
        linestyle='--',
        linewidth=2,
        label=f'Promedio: {exponente_promedio:.2f} ± {error_exponente:.2f}'
    )

    plt.xlabel('Número de serie de medición')
    plt.ylabel('Exponente (p) optimizado')
    plt.title('Distribución de Exponentes por Serie', fontweight='bold')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.savefig('ajuste_ley_potencia.png', dpi=300, bbox_inches='tight')
    plt.show()


def graficar_decaimiento():
    plt.figure(figsize=(10, 6))

    # Vector x suave para graficar las líneas de ajuste de forma continua
    x_suave = np.linspace(x.min(), x.max(), 200)

    idx = 0
    for i in df_pivoteado.columns:
        if i != "distancia":
            y_norm = df_pivoteado[i] / df_pivoteado[i].iloc[0]

            # Puntos experimentales
            plt.scatter(x, y_norm, alpha=0.5, label=f'Serie {i}' if idx < 5 else "")

            # Curva de ajuste individual (en gris tenue para no saturar)
            p_val = exponente[idx]
            #y_ajuste_indiv = ley_de_potencia_normalizada(x_suave, p_val)
            #plt.plot(x_suave / 40, y_ajuste_indiv, linestyle='--', color='gray', alpha=0.25, label='_nolegend_')

            idx += 1

    # Curva teórica evaluada con el exponente promedio
    y_ajuste_promedio = ley_de_potencia_normalizada(x_suave, exponente_promedio)
    Y_teorico=ley_de_potencia_normalizada(x_suave,-2)
    """
    plt.plot(
        x_suave / 40,
        y_ajuste_promedio,
        color='red',
        linewidth=2.5,
        label=f'Ajuste con Promedio ($p = {exponente_promedio:.2f}$)'
    )
    plt.plot(
        x_suave / 40,
        Y_teorico,
        color='blue',
        linewidth=2,
        label='Ley de cuadrado inverso'
    )
    """
    plt.xlabel('L / $L_0$ ($L_0 = 40 cm$)',fontsize=16)
    plt.ylabel('V / $V_0$',fontsize=16)
    #plt.title('Curvas de Decaimiento y Ajuste de Ley de Potencia', fontweight='bold', pad=12)
    plt.legend(loc='upper right', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.savefig('intensidad-distancia-ajuste.png', dpi=300, bbox_inches='tight')
    plt.show()


# Ejecutar gráficos
graficar_decaimiento()
graficar_exponente()