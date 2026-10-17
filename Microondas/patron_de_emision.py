import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("voltaje_angulo_lateral.csv")  # cargo los datos
df_pivoteado = df.pivot(index="angulo", columns="indice", values="voltaje")
df_pivoteado.reset_index(inplace=True)

# Configuración global del tamaño de letra
plt.rcParams.update({'font.size': 14})


def grafica_frente():
    x =df_pivoteado.angulo - 180
    plt.figure(figsize=(10, 6))

    for i in df_pivoteado.columns:
        if i != "angulo":
            y = df_pivoteado[i]
            plt.plot(x, y, marker='', linewidth=2, label=f'Serie {i}')

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

    # 1. Configuramos los límites para que muestre de -90° a 90° (la mitad derecha)
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
            # 2. Restamos 180° para desplazar el rango [90, 270] al rango [-90, 90]
            theta = np.radians(df_pivoteado.angulo - 180)
            r = df_pivoteado[i]
            ax.plot(theta, r, marker='', linewidth=2, label=f'Serie {i}')

    ax.set_rlim(0, max_voltaje * 1.10)

    ax.set_title('Patrón de Radiación ', fontsize=18, fontweight='bold', pad=25)
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize=12)

    plt.tight_layout()
    plt.savefig('patron_radiacion_semipolar.png', dpi=300, bbox_inches='tight')
    plt.show()


# Ejecutar las funciones
grafica_frente()
grafica_frente_polares()