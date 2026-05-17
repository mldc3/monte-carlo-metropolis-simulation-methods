import numpy as np
import matplotlib.pyplot as plt
import random

# -------------------------------
N = 50            # Numero de particulas
KT = 10         # Valor de KT (temperatura)
h = 1             # Lo ponemos con el fin de simplificar
m = 1             # Lo ponemos con el fin de simplificar
L = 1             # Lo ponemos con el fin de simplificar
pasos_MC = 120000  # Numero total de pasos de Monte Carlo
n = np.ones((N, 3), dtype=int) # Al iniciar ponemos que cada particula tiene tres numeros cuanticos y todos son 1

# -------------------------------
#hacemos una función que nos vaya calculando las energías de las partículas
def energia_particula(n_i,h,m,L):
    return h**2*np.pi**2 * (n_i[0]**2 + n_i[1]**2 + n_i[2]**2) / (2*m*L**2)

# Calculamos la nergia total inicial del sistema
E_total = np.sum([energia_particula(n[i],h,m,L) for i in range(N)])

# Cremos una lista para guardar la energia total en cada paso, que empiece con todo 1
E_hist = [E_total]


# -------------------------------
# Generamos una función que lleva a cabo el algoritmo de Metropolis Monte Carlo
for paso in range(pasos_MC):
    # Primero debemos elegir una partícula aleatoria y una dirección de esta (nx, ny, nz)
    particula = random.randrange(N)       #partícula
    d = random.randrange(3)       #dircción
    # Elegimos cambio aleatorio con la función choice (+1 o -1)
    cambio = random.choice([-1, 1])
    # Proponemos nuevo valor para ver si es mayor o menor de 1 y así descartar o no
    nuevo_n = n[particula, d] + cambio
    if nuevo_n < 1:
        continue
    # Calcular energia antes y despues del cambio ya que si es menor nos quedamos con el cambio ya que buscamos el equilibrio
    E_antes = energia_particula(n[particula],h,m,L) #Energía antes del cambio
    n_propuesta = n[particula].copy() #guardamos las propuestas en una lista porque nunca se sabe que pueda pasar 
    n_propuesta[d] = nuevo_n
    E_despues = energia_particula(n_propuesta,h,m,L)
    # Calculamos la diferencia de las energ'ias para ver si nos quedamos con el cambio o no
    delta_E = E_despues - E_antes
    # Ahora aplicamos lo importante del algoritmo vamos a aceptar si delta_E < 0, o con probabilidad exp(-delta_E/KT)
    if delta_E <= 0:
        # Si la energía disminuye, aceptamos el cambio siempre (criterio de Metropolis)
        n[particula, d] = nuevo_n
        E_total += delta_E
    elif np.random.rand() < np.exp(-delta_E / KT):
        # Si la energía aumenta, aceptamos el cambio solo con una probabilidad Boltzmann
        n[particula, d] = nuevo_n
        E_total += delta_E
    
    # Guardar energia total actual
    E_hist.append(E_total)
    
# -------------------------------
#Gráfica 1
plt.figure(figsize=(8,4))
plt.plot(E_hist)
plt.xlabel('Paso de Monte Carlo')
plt.ylabel('Energia total del sistema')
plt.title(f'Evolucion de la energia total (N={N}, KT={KT})')
plt.grid(True)
plt.show()  

  
# -------------------------------
#Gráfica comparación de diferentes valores de KT
KT_lista = [1, 30, 50,100]

plt.figure(figsize=(10,5))

for KT in KT_lista:
    n = np.ones((N, 3), dtype=int)
    E_total = np.sum([energia_particula(n[i],h,m,L) for i in range(N)])
    E_hist = [E_total]
    for paso in range(pasos_MC):
        particula = np.random.randint(N)
        d = np.random.randint(3)
        cambio = np.random.choice([-1, 1])
        nuevo_n = n[particula, d] + cambio
        if nuevo_n < 1:
            continue
        E_antes = energia_particula(n[particula],h,m,L)
        n_propuesta = n[particula].copy()
        n_propuesta[d] = nuevo_n
        E_despues = energia_particula(n_propuesta,h,m,L)
        delta_E = E_despues - E_antes
        if delta_E <= 0:
            n[particula, d] = nuevo_n
            E_total += delta_E
        elif np.random.rand() < np.exp(-delta_E / KT):
            n[particula, d] = nuevo_n
            E_total += delta_E
        E_hist.append(E_total)
    plt.plot(E_hist, label=f'KT={KT}')

plt.xlabel('Paso de Monte Carlo')
plt.ylabel('Energía total del sistema')
plt.title(f'Evolución de la energía total para diferentes KT (N={N})')
plt.legend()
plt.grid(True)
plt.show()
    
    
    
# -------------------------------
#Gráfica comparación de diferentes valores de N
N_lista = [3,10,50,100]

plt.figure(figsize=(10,5))

for N in N_lista:
    n = np.ones((N, 3), dtype=int)
    E_total = np.sum([energia_particula(n[i],h,m,L) for i in range(N)])
    E_hist = [E_total]
    for paso in range(pasos_MC):
        particula = np.random.randint(N)
        d = np.random.randint(3)
        cambio = np.random.choice([-1, 1])
        nuevo_n = n[particula, d] + cambio
        if nuevo_n < 1:
            continue
        E_antes = energia_particula(n[particula],h,m,L)
        n_propuesta = n[particula].copy()
        n_propuesta[d] = nuevo_n
        E_despues = energia_particula(n_propuesta,h,m,L)
        delta_E = E_despues - E_antes
        if delta_E <= 0:
            n[particula, d] = nuevo_n
            E_total += delta_E
        elif np.random.rand() < np.exp(-delta_E / KT):
            n[particula, d] = nuevo_n
            E_total += delta_E
        E_hist.append(E_total)
    plt.plot(E_hist, label=f'N={N}')

plt.xlabel('Paso de Monte Carlo')
plt.ylabel('Energía total del sistema')
plt.title(f'Evolución de la energía total para diferentes número de partículas (KT={KT})')
plt.legend()
plt.grid(True)
plt.show()    





# -------------------------------
#Gráfica comparación de diferentes valores de N
L_lista = [1,3,5,10]

plt.figure(figsize=(10,5))

for L in L_lista:
    n = np.ones((N, 3), dtype=int)
    E_total = np.sum([energia_particula(n[i],h,m,L) for i in range(N)])
    E_hist = [E_total]
    for paso in range(pasos_MC):
        particula = np.random.randint(N)
        d = np.random.randint(3)
        cambio = np.random.choice([-1, 1])
        nuevo_n = n[particula, d] + cambio
        if nuevo_n < 1:
            continue
        E_antes = energia_particula(n[particula],h,m,L)
        n_propuesta = n[particula].copy()
        n_propuesta[d] = nuevo_n
        E_despues = energia_particula(n_propuesta,h,m,L)
        delta_E = E_despues - E_antes
        if delta_E <= 0:
            n[particula, d] = nuevo_n
            E_total += delta_E
        elif np.random.rand() < np.exp(-delta_E / KT):
            n[particula, d] = nuevo_n
            E_total += delta_E
        E_hist.append(E_total)
    plt.plot(E_hist, label=f'L={L}')

plt.xlabel('Paso de Monte Carlo')
plt.ylabel('Energía total del sistema')
plt.title(f'Evolución de la energía total para diferentes tamaños de caja (N={N} y KT={KT})')
plt.legend()
plt.grid(True)
plt.show() 










    



