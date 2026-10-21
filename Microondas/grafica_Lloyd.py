import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 1. Diccionario con los tres archivos específicos
archivos_grafico = {
    "Placa 6 cm ": "reflexion_metal_6cm(1).csv",
    "Placa 9 cm ": "reflexion_metal_9cm(1).csv",
    "Placa 15 cm": "reflexion_metal_15.2cm_71cm.csv"
}

# 2. Configuración general para letras grandes
plt.figure(figsize=(10, 6))
plt.rcParams.update({'font.size': 14})

# 3. Procesar, normalizar y graficar cada archivo
for nombre, archivo in archivos_grafico.items():
    df = pd.read_csv(archivo)
    df.columns = df.columns.str.strip()

    # Pivotear para organizar por distancia
    df_piv = df.pivot(index="distancia", columns="indice", values="voltaje")
    df_piv.reset_index(inplace=True)

    distancias = df_piv["distancia"].values

    # Promediar las columnas de voltaje
    columnas_voltaje = [c for c in df_piv.columns if c != "distancia"]
    voltaje_promedio = df_piv[columnas_voltaje].mean(axis=1).values

    # --- NORMALIZACIÓN MIN-MAX (Escala de 0 a 1) ---
    v_min = np.nanmin(voltaje_promedio)
    v_max = np.nanmax(voltaje_promedio)
    voltaje_norm = (voltaje_promedio - v_min) / (v_max - v_min)

    # Graficar curva normalizada
    plt.plot(distancias, voltaje_norm, label=nombre, linewidth=2)

# 4. Formato del gráfico (sin título, con etiquetas y leyendas solicitadas)
plt.xlabel("h[cm]", fontsize=18)
plt.ylabel("V[v]", fontsize=18)
plt.legend(fontsize=16)
plt.grid(True, linestyle="--", alpha=0.7)
plt.tight_layout()

# Mostrar el gráfico
plt.show()