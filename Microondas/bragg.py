import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks

# 1. Cargar y pivotear los datos
df = pd.read_csv("bragg.csv")
# Limpiar nombres de columnas por seguridad
df.columns = df.columns.str.strip()

df_pivot = df.pivot(index="angulo", columns="indice", values="voltaje")
df_pivot.reset_index(inplace=True)

# Parámetros iniciales
d = 3.8  # Distancia interplanar (cm)
lambda_teorica = 2.85  # cm

angles = df_pivot["angulo"].values
columnas_indice = [c for c in df_pivot.columns if c != "angulo"]

# Lista para almacenar todas las longitudes de onda calculadas experimentalmente
lambdas_experimentales = []

print("=== LONGITUDES DE ONDA CALCULADAS POR PICO ===")

# 2. Detección de picos y cálculo de lambda por cada medición
for col in columnas_indice:
    voltaje = df_pivot[col].values

    # Manejar posibles valores nulos
    valido = ~np.isnan(voltaje)
    ang_val = angles[valido]
    volt_val = voltaje[valido]

    if len(volt_val) < 5:
        continue

    # Encontrar los picos (máximos) en la curva de Bragg
    picos_idx, _ = find_peaks(volt_val, prominence=0.1)
    angulos_picos = ang_val[picos_idx]

    # Calcular lambda para cada pico detectado
    # m es el orden del pico (asumimos orden 1, 2, 3... según la posición del pico)
    for idx, theta_deg in enumerate(angulos_picos):
        m = idx + 1 # Orden de difracción (1er pico -> m=1, 2do -> m=2, etc.)
        theta_rad = np.radians(theta_deg)

        # Ley de Bragg: m * lambda = 2 * d * sin(theta) => lambda = (2 * d * sin(theta)) / m
        lam_calc = (2 * d * np.sin(theta_rad)) / m
        lambdas_experimentales.append(lam_calc)

        print(f"Ensayo {col} | Pico m={m} en θ={theta_deg:.2f}° -> λ = {lam_calc:.3f} cm")

# Promedio global de las longitudes de onda experimentales
if lambdas_experimentales:
    lambda_promedio = np.mean(lambdas_experimentales)
    lambda_std = np.std(lambdas_experimentales, ddof=1)
    print("\n----------------------------------------")
    print(f"Promedio experimental de λ: {lambda_promedio:.3f} cm")
    print(f"Desviación estándar:       {lambda_std:.3f} cm")
    print("----------------------------------------")
else:
    print("\nNo se detectaron suficientes picos. Revisa el parámetro 'prominence' o tus datos.")


# 3. Gráfica de los datos y líneas teóricas de referencia
def thetas_teoricos(l_in):
    angs = []
    for i in range(10):
        argumento = (i * l_in) / (2 * d)
        if argumento > 1:
            break
        ang = np.arcsin(argumento)

        if ang <= np.pi/4:
            angs.append(ang * (180 / np.pi))
            continue
        else:
            break
    return angs


ang_max = thetas_teoricos(lambda_teorica)

plt.figure(figsize=(10, 6))
plt.rcParams.update({'font.size': 14})

# Graficar líneas verticales teóricas
for i, ang in enumerate(ang_max):
    if i > 0:  # Ignorar el orden m=0 en 0° si aparece
        plt.axvline(ang, color='red', linestyle='--', alpha=0.6, label='Teórico (Bragg)' if i == 1 else "")

# Graficar las curvas experimentales para cada índice
for col in columnas_indice:
    plt.plot(df_pivot["angulo"], df_pivot[col], alpha=0.7, label=f"Tanda {col}")

plt.xlabel("$\\beta$ [°]", fontsize=18)
plt.ylabel("V [v]", fontsize=18)
plt.legend(fontsize=18)
plt.grid(True, linestyle="--", alpha=0.7)
plt.tight_layout()
plt.show()