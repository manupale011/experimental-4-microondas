import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from scipy.integrate import simpson

df = pd.read_csv("voltaje_angulo_lateral.csv")  # cargo los datos
df_pivoteado = df.pivot(index="angulo", columns="indice", values="voltaje")
df_pivoteado.reset_index(inplace=True)

# Configuración global del tamaño de letra
plt.rcParams.update({'font.size': 14})


def grafica_frente():
    x = df_pivoteado.angulo - 180
    plt.figure(figsize=(10, 6))

    for i in df_pivoteado.columns:
        if i != "angulo":
            y = df_pivoteado[i]
            plt.plot(x, y, marker='s', linewidth=2, label=f'Serie {i}')

    plt.title('Voltaje en función del Ángulo (Lateral)', fontsize=18, fontweight='bold', pad=15)
    plt.xlabel('Ángulo (º)', fontsize=16, labelpad=10)
    plt.ylabel('Voltaje (V)', fontsize=16, labelpad=10)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(title='Medición', fontsize=12, title_fontsize=14, loc='best')
    plt.tight_layout()
    plt.savefig('voltaje_vs_angulo_lateral.png', dpi=300, bbox_inches='tight')
    plt.show()


def grafica_frente_polares():
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(10, 8))

    # --- CORRECCIÓN DE ORIENTACIÓN POLAR ---
    # 1. Poner el 0° arriba (Norte)
    ax.set_theta_zero_location("N")
    # 2. Sentido horario para que los ángulos negativos vayan a la izquierda y positivos a la derecha
    ax.set_theta_direction(-1)
    # --------------------------------------

    # 3. Configuramos los límites del abanico visible de -45° a 45°
    ax.set_thetamin(-45)
    ax.set_thetamax(45)

    max_voltaje = 0
    for i in df_pivoteado.columns:
        if i != "angulo":
            val_max_serie = df_pivoteado[i].max()
            if val_max_serie > max_voltaje:
                max_voltaje = val_max_serie

    for i in df_pivoteado.columns:
        if i != "angulo":
            # Restamos 180° para desplazar el rango al sistema centrado en el cero del emisor
            theta = np.radians(df_pivoteado.angulo - 180)
            r = df_pivoteado[i]
            ax.plot(theta, r, marker='s', linewidth=2, label=f'Serie {i}')

    ax.set_rlim(0, max_voltaje * 1.10)

    ax.set_title('$\\beta$[°]', fontsize=18, fontweight='bold', pad=25)
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend(loc='upper right', fontsize=12)

    ax.set_ylabel(r'V[v]',fontsize=18, labelpad=20)  # Leyenda al eje radial

    # Opcional: Ajustar las marcas de los ángulos para mayor claridad en el borde
    ticks_grados = np.array([-45, -30, -15, 0, 15, 30, 45])
    ax.set_xticks(np.radians(ticks_grados))
    ax.set_xticklabels([f'{int(t)}$\\circ$' for t in ticks_grados])

    plt.tight_layout()
    plt.savefig('patron_radiacion_semipolar.png', dpi=300, bbox_inches='tight')
    plt.show()

# Para ejecutar las funciones:
# grafica_frente()
grafica_frente_polares()