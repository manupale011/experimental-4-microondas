import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

# Configuración general para letras grandes
plt.rcParams.update({'font.size': 14})

# 1. Cargar los archivos
archivos = {
    "Placa 6 cm": "reflexion_metal_6cm.csv",
    "Placa 9 cm": "reflexion_metal_9cm.csv",
    "Placa 15 cm": "reflexion_metal_15.2cm_71cm.csv",
    "Placa 6 cm (v2)": "reflexion_metal_6cm(1).csv",
    "Placa 9 cm (v2)": "reflexion_metal_9cm(1).csv"
}

dfs = {}
for nombre, archivo in archivos.items():
    dfs[nombre] = pd.read_csv(archivo)

dfs_pivoteados = {}
for nombre, dataframe in dfs.items():
    dataframe.columns = dataframe.columns.str.strip()
    dfs_pivoteados[nombre] = dataframe.pivot(index="distancia", columns="indice", values="voltaje")
    dfs_pivoteados[nombre].reset_index(inplace=True)


def long_de_onda(h):
    '''
    Calcula la longitud de onda para cada par sucesivo de máximos y mínimos.
    '''
    l = []
    for i in range(1, len(h)):
        long = 2 * (np.sqrt(71 ** 2 + 4 * h[i] ** 2) - np.sqrt(71 ** 2 + 4 * h[i - 1] ** 2))
        l.append(long)
    return l


# Listas y diccionarios para almacenar los resultados
todas_las_lambdas = []
resultados_por_archivo = {}

for nombre, df in dfs_pivoteados.items():
    distancias = df["distancia"].values
    columnas_indice = [c for c in df.columns if c != "distancia"]

    lambdas_este_archivo = []

    print(f"=== {nombre} ===")

    # Procesar cada columna (medición/índice) individualmente
    for col in columnas_indice:
        voltaje = df[col].values

        # Manejar posibles valores nulos (NaN)
        valido = ~np.isnan(voltaje)
        dist_val = distancias[valido]
        volt_val = voltaje[valido]

        if len(volt_val) < 5:
            continue

        # 1. Encontrar picos (máximos y mínimos) para ESTA medición
        picos_max, _ = find_peaks(volt_val, prominence=0.01)
        picos_min, _ = find_peaks(-volt_val, prominence=0.01)

        h_max = dist_val[picos_max]
        h_min = dist_val[picos_min]

        # Unir y ordenar las posiciones en orden creciente
        h = np.sort(np.concatenate([h_max, h_min]))

        if len(h) < 2:
            continue

        # 2. Calcular la longitud de onda para esta medición
        lambdas_medicion = long_de_onda(h)

        # Acumular
        lambdas_este_archivo.extend(lambdas_medicion)
        todas_las_lambdas.extend(lambdas_medicion)

    # Promedio por archivo
    promedio_archivo = np.mean(lambdas_este_archivo) if lambdas_este_archivo else np.nan
    resultados_por_archivo[nombre] = {
        "lambdas": lambdas_este_archivo,
        "promedio": promedio_archivo
    }
    print(f"  -> Longitudes de onda calculadas: {len(lambdas_este_archivo)}")
    print(f"  -> Promedio del archivo: {promedio_archivo:.3f} cm\n")

# 3. Promedio global y desviación estándar de todas las mediciones
if todas_las_lambdas:
    promedio_global = np.mean(todas_las_lambdas)
    desviacion_global = np.std(todas_las_lambdas, ddof=1)

    print("========================================")
    print("           RESULTADO GLOBAL             ")
    print("========================================")
    print(f"Cantidad total de valores de lambda: {len(todas_las_lambdas)}")
    print(f"Promedio global de longitud de onda: {promedio_global:.3f} cm")
    print(f"Desviación estándar global (std):    {desviacion_global:.3f} cm")
    print("========================================")
else:
    print("No se pudieron calcular longitudes de onda. Revisa los parámetros de los picos.")

# ========================================
# 4. GRÁFICO DE TODAS LAS LONGITUDES DE ONDA
# ========================================
plt.figure(figsize=(12, 6))

# Graficar los valores de lambda agrupados por cada placa con un pequeño desplazamiento aleatorio en X (jitter) para que no se superpongan
for i, (nombre, datos) in enumerate(resultados_por_archivo.items()):
    lambdas = datos["lambdas"]
    if len(lambdas) > 0:
        # Añadir un pequeño "jitter" horizontal artificial para visualizar puntos repetidos
        x_vals = np.random.normal(i, 0.04, size=len(lambdas))
        plt.scatter(x_vals, lambdas, alpha=0.7, s=50)

# Línea horizontal indicando el promedio global
plt.axhline(promedio_global, color='red', linestyle='--', linewidth=2,
            label=f'Promedio Global: {promedio_global:.2f} cm')
plt.axhline(2.85, color='green', linestyle='-', linewidth=2,
            label='Valor de fábrica: 2.85 cm')

# Configuración de ejes y etiquetas
nombres_placas = list(resultados_por_archivo.keys())
plt.xticks(range(len(nombres_placas)), nombres_placas, rotation=15, fontsize=18)
plt.ylabel("$\\lambda$ [cm]", fontsize=18)
plt.legend(fontsize=18, loc='lower right')
plt.grid(True, linestyle="--", alpha=0.5)
plt.xlim(-0.5, len(nombres_placas) - 0.5)
plt.tight_layout()

plt.show()