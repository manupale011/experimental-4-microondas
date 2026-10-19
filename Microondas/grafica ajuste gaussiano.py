import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.integrate import simpson

df = pd.read_csv("voltaje_angulo_lateral.csv")  # cargo los datos
df_pivoteado = df.pivot(index="angulo", columns="indice", values="voltaje")
df_pivoteado.reset_index(inplace=True)
df_pivoteado.angulo=df_pivoteado.angulo-180


def ajuste_y_grafico_gaussiana(df_pivoteado):
    resultados = []

    for col in df_pivoteado.columns:
        if col != "angulo":
            # 1. Limpieza de datos
            datos = df_pivoteado[['angulo', col]].dropna()
            theta = datos['angulo'].values
            v = datos[col].values

            if len(v) < 5:  # Necesitamos al menos 5 puntos para 4 parámetros
                continue

            # 2. Estimaciones iniciales
            idx_max = np.argmax(v)
            h_init = v[idx_max]
            theta0_init = theta[idx_max]
            c_init = np.mean(v[-3:])

            v_neto = v - c_init
            integral = simpson(v_neto, theta)
            if np.min(theta) >= -1e-5:  # Si el barrido es de 0 a 50°
                integral *= 2

            a0 = integral / (h_init * np.sqrt(2 * np.pi))
            if a0 <= 0:
                a0 = 10.0

                # 3. Definición de la función

            def gaussiana_con_offset(angle, h, theta_0, a, c):
                return h * np.exp(-((angle - theta_0) ** 2) / (2 * a ** 2)) + c

            try:
                # 4. Ajuste con curve_fit
                p, cov = curve_fit(
                    gaussiana_con_offset,
                    theta,
                    v,
                    p0=[h_init, theta0_init, a0, c_init],
                    bounds=([0, -180, 0, -np.inf], [np.inf, 180, np.inf, np.inf])
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

                # --- 5. GRÁFICO COMPARATIVO ---
                plt.figure(figsize=(8, 5))

                # Puntos experimentales
                plt.scatter(theta, v, color='blue', label='Datos experimentales', zorder=5, s=35)

                # Curva teórica ajustada (suave)
                theta_smooth = np.linspace(theta.min(), theta.max(), 500)
                v_fit = gaussiana_con_offset(theta_smooth, h_fit, theta0_fit, a_fit, c_fit)
                plt.plot(theta_smooth, v_fit, color='red', linewidth=2,
                         label=f'Ajuste (a={a_fit:.2f}°, c={c_fit:.2f}V)')

                # Estética del gráfico
                plt.axhline(0, color='gray', linestyle='--', alpha=0.5)
                plt.title(f'Patrón de Emisión - Columna: {col}')
                plt.xlabel(r'Ángulo ($\circ$)')
                plt.ylabel('Voltaje (V)')
                plt.grid(True, linestyle=':', alpha=0.7)
                plt.legend()
                plt.tight_layout()
                plt.show()

            except Exception as e:
                print(f"No se pudo ajustar la columna {col}: {e}")

    return pd.DataFrame(resultados)

ajuste_y_grafico_gaussiana(df_pivoteado)