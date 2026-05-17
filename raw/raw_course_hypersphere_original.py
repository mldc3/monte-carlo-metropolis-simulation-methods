import numpy as np
import matplotlib.pyplot as plt
from random import uniform
from scipy.special import gamma

"""
Objetivo del código:
Primero, se calcula el área de un círculo (2D) de radio 1 para ilustrar el método.
Luego, se generaliza a N dimensiones (ejemplo: 10 dimensiones). 
La idea es generar puntos aleatorios dentro del hiper-cubo que contiene la esfera 
y contar la fracción de puntos que caen dentro de la hiperesfera. 
Multiplicando por el volumen del hiper-cubo obtenemos una estimación del volumen.
"""

import numpy as np
import matplotlib.pyplot as plt
from random import uniform  # Genera números aleatorios uniformes

# -------------------------------
# Función que verifica si un punto está dentro de la hiperesfera
def dentro_esfera(punto, radio):
    # Calculamos la suma de los cuadrados de las coordenadas
    # Si es menor o igual que radio^2, el punto está dentro
    return sum(x**2 for x in punto) <= radio**2

# -------------------------------
# Función que calcula el volumen mediante Monte Carlo
def volumen_MC(dimensiones, radio, N):
    dentro = 0  # Contador de puntos que caen dentro de la hiperesfera

    for _ in range(N):
        # Generamos un punto aleatorio dentro del hiper-cubo [-radio, radio]^dimensiones
        punto = [uniform(-radio, radio) for i in range(dimensiones)]
        
        # Miramos si el punto está dentro de la hiperesfera
        if dentro_esfera(punto, radio):
            dentro += 1  # Incrementamos el contador si está dentro

    # Calculamos el volumen del hiper-cubo que contiene la hiperesfera
    V_cubo = (2 * radio)**dimensiones
    
    # La fracción de puntos dentro de la esfera multiplicada por el volumen del hiper-cubo
    # nos da una estimación del volumen de la hiperesfera
    V_esfera = (dentro / N) * V_cubo
    
    return V_esfera

# -------------------------------
# Ejemplo 1: área de un círculo (2D) de radio 1
radio = 1
dimensiones = 2
N = 100000  # Número de puntos Monte Carlo

vol2D = volumen_MC(dimensiones, radio, N)
print(f"Área aproximada del círculo (2D, radio={radio}): {vol2D:.6f} (π ≈ {np.pi:.6f})")

# -------------------------------
# Ejemplo 2: hiperesfera de 5 dimensiones
dimensiones = 5
vol10D = volumen_MC(dimensiones, radio, N)
print(f"Volumen aproximado de la hiperesfera 5D (radio={radio}): {vol10D:.6f}")

# -------------------------------
# Ejemplo 3: hiperesfera de 8 dimensiones
dimensiones = 8
vol10D = volumen_MC(dimensiones, radio, N)
print(f"Volumen aproximado de la hiperesfera 8D (radio={radio}): {vol10D:.6f}")


# -------------------------------
# Ejemplo 4: hiperesfera de 10 dimensiones
dimensiones = 10
vol10D = volumen_MC(dimensiones, radio, N)
print(f"Volumen aproximado de la hiperesfera 10D (radio={radio}): {vol10D:.6f}")



# -------------------------------
# Ahora vamos a ver cómo depende del número de dimensión
radio = 1
N = 100000  # número de puntos Monte Carlo
dimensiones_max = 15
dimensiones_array = np.arange(1, dimensiones_max + 1)  # de 1 a 15 dimensiones
valores_MC = []

# -------------------------------
# Calculamos el volumen estimado para cada dimensión
for dim in dimensiones_array:
    vol = volumen_MC(dim, radio, N)
    valores_MC.append(vol) 

# -------------------------------
# Graficamos el volumen estimado vs número de dimensiones
plt.figure()
plt.plot(dimensiones_array, valores_MC, 'o-', color='blue', label="Volumen estimado")
plt.xlabel("Número de dimensiones")
plt.ylabel("Volumen estimado")
plt.title("Volumen de hiperesfera de radio 1 vs dimensiones (Monte Carlo)")
plt.grid(True)
plt.legend()
plt.show()


# -------------------------------
# Calculo del volumen exacto con formula analitica
def volumen_real(dimensiones, radio):
    return (np.pi**(dimensiones/2) / gamma(dimensiones/2 + 1)) * (radio**dimensiones)

# -------------------------------
# Calculamos los errores relativos para cada dimension
valores_reales = [volumen_real(dim, radio) for dim in dimensiones_array]
errores_relativos = [abs((mc - real) / real) for mc, real in zip(valores_MC, valores_reales)]

# -------------------------------
# Graficamos el error relativo vs numero de dimensiones
plt.figure()
plt.plot(dimensiones_array, errores_relativos, 'o-r', label="Error relativo")
plt.xlabel("Numero de dimensiones")
plt.ylabel("Error relativo")
plt.title("Error relativo en el calculo del volumen de la hiperesfera")
plt.grid(True)
plt.legend()
plt.show()