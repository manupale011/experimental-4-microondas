import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
from scipy.integrate import simpson

df = pd.read_csv("voltaje_angulo_lateral.csv")  # cargo los datos
df_pivoteado = df.pivot(index="angulo", columns="indice", values="voltaje")
df_pivoteado.reset_index(inplace=True)
df_pivoteado.angulo=df_pivoteado.angulo-180

def ajuste_gaussiana_con_offset(df_pivoteado):
    resultados = []

    for col in df_pivoteado.columns:
        if col != "angulo":
            # 1. Limpieza de datos
            datos = df_pivoteado[['angulo', col]].dropna()
            theta = datos['angulo'].values
            v = datos[col].values

            if len(v) < 5:  # Necesitamos al menos 5 puntos para ajustar 4 parámetros
                continue

            # 2. Estimaciones iniciales inteligentes
            idx_max = np.argmax(v)
            h_init = v[idx_max]  # Máximo medido
            theta0_init = theta[idx_max]  # Ángulo del pico (desalineación)

            # Estimación del offset c: tomamos el promedio de los últimos 3 puntos (extremos del barrido)
            c_init = np.mean(v[-3:])

            # Restamos el offset a los datos para estimar la integral de la campana "limpia"
            v_neto = v - c_init
            integral = simpson(v_neto, theta)
            if np.min(theta) >= -1e-5:  # Si solo mide de 0 a 50°
                integral *= 2

            a0 = integral / (h_init * np.sqrt(2 * np.pi))
            if a0 <= 0:  # Control por si acaso la estimación da negativa
                a0 = 10.0

                # 3. Función Gaussiana con offset constante

            def gaussiana_con_offset(angle, h, theta_0, a, c):
                return h * np.exp(-((angle - theta_0) ** 2) / (2 * a ** 2)) + c

            try:
                # 4. Ajuste con curve_fit (4 parámetros)
                p, cov = curve_fit(
                    gaussiana_con_offset,
                    theta,
                    v,
                    p0=[h_init, theta0_init, a0, c_init],
                    bounds=([0, -180, 0, -np.inf], [np.inf, 180, np.inf, np.inf])  # h>0, a>0
                )

                h_fit, theta0_fit, a_fit, c_fit = p
                errores = np.sqrt(np.diag(cov))

                resultados.append({
                    'columna': col,
                    'a': a_fit,
                    'error_a': errores[2],
                    'theta_0': theta0_fit,
                    'error_theta_0': errores[1],
                    'h': h_fit,
                    'error_h': errores[0],
                    'offset_c': c_fit,
                    'error_c': errores[3]
                })

                print(f"Col {col}: a = {a_fit:.3f}, desalineación = {theta0_fit:.2f}°, offset = {c_fit:.3f} V")

            except Exception as e:
                print(f"No se pudo ajustar {col}: {e}")

    return pd.DataFrame(resultados)

# 1. Ejecutas la función para obtener los resultados de todas las columnas
df_resultados = ajuste_gaussiana_con_offset(df_pivoteado)

# 2. Seleccionas las mediciones que quieres promediar (1, 2 y 3)
# Nota: Si tus columnas son strings (ej. '1', '2', '3'), cambia los números por texto: ['1', '2', '3']
mediciones_objetivo = [1, 2, 3]

# Filtramos el DataFrame de resultados para quedarnos solo con esas filas
df_subset = df_resultados[df_resultados['columna'].isin(mediciones_objetivo)]

# 3. Calculamos el promedio (mean) y la desviación estándar muestral (std) de los parámetros
promedios = df_subset[['a', 'theta_0', 'h', 'offset_c']].mean()
desviaciones = df_subset[['a', 'theta_0', 'h', 'offset_c']].std()

print("--- PROMEDIO DE LAS MEDICIONES 1, 2 y 3 ---")
print(promedios)

print("\n--- DESVIACIÓN ESTÁNDAR ENTRE MEDICIONES ---")
print(desviaciones)