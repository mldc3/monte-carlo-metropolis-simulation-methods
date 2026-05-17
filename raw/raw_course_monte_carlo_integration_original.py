import numpy as np
import matplotlib.pyplot as plt
from random import uniform
from scipy.integrate import quad

# -------------------------------
# Definimos función

def f(x):
    return np.sin(1 / (x * (2 - x))) ** 2
'''
def f(x):
    return (np.e**(x**2))/((x-24)**2+0.024)
'''
# Intervalo
a, b = 0, 2
x = np.linspace(0.001, 1.999, 500)  # evitamos singularidades
y = f(x)

# -------------------------------
# 1. Representamos f(x)
plt.figure()
plt.plot(x, y, 'b', label=r'$f(x) = \sin^2\left(\frac{1}{x(2-x)}\right)$')
#plt.plot(x, y, 'b', label=r'$f(x) = \frac{e^{x^2}}{(x-24)^2 + 0.024}$')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.title('Gráfica de $f(x)$ en $[0, 2]$')
plt.legend()
plt.grid(True)
plt.show()

# -------------------------------
# Encontramos el máximo aproximado de la función
ymax = np.max(y) * 1.01  # margen de seguridad
print("Máximo de la función estimado:", ymax)

# -------------------------------
# 2. Monte Carlo
def dentro_o_fuera(a, b, ymax):
    xrand = uniform(a, b)
    yrand = uniform(0, ymax)
    if yrand < f(xrand):
        return True, xrand, yrand
    else:
        return False, xrand, yrand

def integral_MC(a, b, ymax, N):
    dentro = 0
    x_in, y_in, x_out, y_out = [], [], [], []
    for _ in range(N):
        ok, xr, yr = dentro_o_fuera(a, b, ymax)
        if ok:
            dentro += 1
            x_in.append(xr)
            y_in.append(yr)
        else:
            x_out.append(xr)
            y_out.append(yr)
    integral = (dentro / N) * (b - a) * ymax
    return integral, x_in, y_in, x_out, y_out

# Valor exacto con quad
valor_real, _ = quad(f, 0, 2)
print("Valor real de la integral:", valor_real)

# -------------------------------
# 3. Integral y error en función de N
Npasos = np.logspace(2, 4, 1000, dtype=int)  # desde 100 hasta 10000
valores_MC = []
errores = []

for N in Npasos:
    integral, _, _, _, _ = integral_MC(a, b, ymax, N)
    valores_MC.append(integral)
    error = abs(integral - valor_real)
    errores.append(error)
    print(f"N={N:6d} -> Integral MC = {integral:.6f} | Error = {error:.6f}")

# Gráfica de la integral vs N
plt.figure()
plt.errorbar(Npasos, valores_MC, fmt='o-', label="Monte Carlo")
plt.axhline(valor_real, color='r', linestyle='--', label="Valor real")
plt.xlabel("Número de pasos N")
plt.ylabel("Valor de la integral")
plt.title("Aproximación Monte Carlo de la integral")
plt.legend()
plt.grid(True)
plt.show()


# Gráfica del error
plt.figure()
plt.plot(Npasos, errores, 'o-', label="Error absoluto")
plt.xlabel("Número de pasos N")
plt.ylabel("Error |MC - exacto|")
plt.title("Error de Monte Carlo vs N")
plt.legend()
plt.grid(True)
plt.show()


# -------------------------------
# 4. Representar función con puntos aceptados y rechazados
N_mostrar = 5000  # número de puntos para la gráfica
_, x_in, y_in, x_out, y_out = integral_MC(a, b, ymax, N_mostrar)

plt.figure()
plt.plot(x, y, 'k', label="f(x)")
plt.scatter(x_in, y_in, s=5, color='green', alpha=0.5, label="Aceptados")
plt.scatter(x_out, y_out, s=5, color='red', alpha=0.5, label="Rechazados")
plt.xlabel("x")
plt.ylabel("f(x)")
plt.title("Muestreo Monte Carlo en $[0,2]$")
plt.legend()
plt.grid(True)
plt.show()


# -------------------------------
# 5. Comparacion con diferentes valores de ymax
ymax_centro = ymax   # maximo real            
ymax_mayor  = ymax * 1.15  # aumentamos un 15 por ciento el valor del maximo
ymax_menor  = ymax * 0.85  # disminuimos un 15 por ciento el valor del maximo

val_MC_centro, val_MC_mayor, val_MC_menor = [], [], [] # creamos listas para guardar valores
Npasos = np.logspace(2, 4, 200, dtype=int)   # numero de pasos que tendra nuestra iteracion

for N in Npasos:
    val_c = integral_MC(a, b, ymax_centro, N)[0]  # obtenemos valores con ymax esperado  
    val_mas = integral_MC(a, b, ymax_mayor, N)[0]  # obtenemos valores con ymax mayor  
    val_menos = integral_MC(a, b, ymax_menor, N)[0]  # obtenemos valores con ymax menor  

    # guardamos en la lista para graficar
    val_MC_centro.append(val_c)
    val_MC_mayor.append(val_mas)
    val_MC_menor.append(val_menos)

# -------------------------------
# Grafica comparativa
plt.figure(figsize=(8,5))
plt.plot(Npasos, val_MC_centro, '-', label=r'$ymax =$ valor estimado')
plt.plot(Npasos, val_MC_mayor,  '-', label=r'$ymax= 1.15 \times$ estimado')
plt.plot(Npasos, val_MC_menor,  '-', label=r'$ymax = 0.85 \times$ estimado')
plt.axhline(valor_real, color='r', linestyle='--', label="Valor real")

plt.xlabel("Numero de pasos N")
plt.ylabel("Valor estimado de la integral")
plt.title("Efecto del valor de M en Monte Carlo por rechazo")
plt.legend()
plt.grid(True, which="both")
plt.show()

