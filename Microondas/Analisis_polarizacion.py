import pandas as pd
import matplotlib.pyplot as plt

df=pd.read_csv("voltaje_angulo_polarizacion.csv") #subo los datos
df_pivoteado=df.pivot(index='angulo', columns='indice', values='voltaje') # separo las distintas tandas en columnas distintas
df_pivoteado=df_pivoteado.reset_index() #reinicio el indice para que los angulos queden en una columna aparte

def grafica_voltaje_angulo():
    x=df_pivoteado.angulo
    plt.rcParams.update({'font.size': 14})  # Aumenta el tamaño base de la letra
    plt.figure(figsize=(10,6))
    for i in df_pivoteado.columns:
        if i != "angulo":
            y=df_pivoteado[i]
            plt.plot(x,y,marker='', linewidth=2, label=f'Serie {i}')

    plt.title('Dependencia del Voltaje con el Ángulo de Polarización', fontsize=18, fontweight='bold', pad=15)
    plt.xlabel('Ángulo (º)', fontsize=16, labelpad=10)
    plt.ylabel('Voltaje (V)', fontsize=16, labelpad=10)

    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)

    plt.grid(True,linestyle='--', alpha=0.7)
    plt.legend(title='Medición', fontsize=12, title_fontsize=14, loc='best')

    plt.tight_layout()  # Ajusta automáticamente los márgenes para que no se corte el texto
    plt.show()

grafica_voltaje_angulo()
