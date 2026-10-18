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

for nombre, archivo in archivos.items():
    dfs[nombre] = pd.read_csv(archivo)

dfs_pivoteados = {}

for nombre, dataframe in dfs.items():
    # Limpiamos espacios por seguridad
    dataframe.columns = dataframe.columns.str.strip()

    dfs_pivoteados[nombre] = dataframe.pivot(index="distancia", columns="indice", values="voltaje")
    dfs_pivoteados[nombre].reset_index(inplace=True)

# Configuración global del tamaño de letra para que se vea grande y legible
plt.rcParams.update({'font.size': 14})


def grafica_distancia_voltaje():
    print("\nArchivos disponibles:", list(dfs_pivoteados.keys()))
    nombre = input("Elija qué gráfica quiere: ")

    # Verificamos primero si existe para evitar errores
    if nombre in dfs_pivoteados:
        df_plot = dfs_pivoteados[nombre]
        x = df_plot.distancia

        plt.figure(figsize=(10, 6))

        for i in df_plot.columns:
            if i != "distancia":
                y = df_plot[i]
                plt.plot(x, y, marker='o', linewidth=2, label=f'Medición {i}')

        # --- DETALLES AGREGADOS ---
        plt.title(f'Interferencia por Placa Metálica ({nombre})', fontsize=18, fontweight='bold', pad=15)
        plt.xlabel('Distancia (cm)', fontsize=16, labelpad=10)
        plt.ylabel('Voltaje', fontsize=16, labelpad=10)
        plt.xticks(fontsize=14)
        plt.yticks(fontsize=14)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend(title='Serie', fontsize=12, title_fontsize=14, loc='best')
        plt.tight_layout()

        # Guardar automáticamente la imagen con el nombre del dataset elegido
        nombre_archivo = f'interferencia_{nombre}.png'
        plt.savefig(nombre_archivo, dpi=300, bbox_inches='tight')
        print(f"-> Gráfico guardado exitosamente como: {nombre_archivo}")

        plt.show()
    else:
        print("❌ Error: El nombre ingresado no es válido. Intente de nuevo.")


# Llamas a la función las veces que necesites
grafica_distancia_voltaje()
grafica_distancia_voltaje()
grafica_distancia_voltaje()
grafica_distancia_voltaje()