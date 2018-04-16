import numpy as np
import matplotlib.pyplot as plt
import sys

def F2(x, inv):
    # inv bool
    # True para fourier inversa
    # False para fourier normal
    M = np.size(x,1)
    N = np.size(x,0)
    Y = np.zeros((N,M), dtype=complex)
    
    Ma = np.array(range(0,M))
    Na = np.array(range(0,N))
    
    m,n = np.meshgrid(Ma,Na)
    
    i = -1
    if(inv):
        i = 1
        
    for k in range(N):
        for l in range(M):
            Y[k,l] = np.sum(x*np.exp(-i*1j*2*np.pi*(n*k/N+m*l/M)), (0,1) ) 
    if (inv):
        Y = Y*1/(M*N)
    return m,n,Y

def reordenar(X,n0,n1):
    return np.roll( np.roll(X,int(n0/2),0), int(n1/2),1 )

argv = sys.argv
bajas = argv[2] == "bajas"
nombre_imagen = argv[1]
I = plt.imread(nombre_imagen)
I = I[50:100,:200] # La imagen es muy grande. Recorto una parte pequeña para no demorarme
m,n,FI2 = F2(I, False)


M = np.size(I,1)
N = np.size(I,0)
m = np.arange(-M/2,M/2)
n = np.arange(-N/2,N/2)
m,n = np.meshgrid(m,n) # grilla para usar en filtros
m = reordenar(m, N,M)
n = reordenar(n, N,M)

# Crear filtros
F_low = np.zeros( (np.size(n,0),np.size(n,1)) )
F_high = np.zeros( (np.size(n,0),np.size(n,1)) )

# frecuencias de corte
w1 = 15
w2 = 25
Dw = w2-w1
pendiente = -1.0/Dw
intercepto1 = -w2/Dw
intercepto2 = w1/Dw

# Definir zonas constantes
F_low[m**2+n**2 < w1**2] = 1.0
F_high[m**2+n**2 < w1**2] = 0.0

F_low[m**2+n**2 > w2**2] = 0.0
F_high[m**2+n**2 > w2**2] = 1.0

# Definir transicion como linea recta
ii = np.logical_and(m**2+n**2>w1**2,m**2+n**2<w2**2)
F_low[ii] = pendiente*((m**2+n**2)**0.5)[ii] - intercepto1
F_high[ii] = -pendiente*((m**2+n**2)**0.5)[ii] - intercepto2

# Usar los filtros sobre el espectro original
FI_low = FI2*F_low
FI_high = FI2*F_high



f,ax = plt.subplots()

if bajas==True:
	m,n,IF_low = F2(FI_low, True)
	ax.imshow(IF_low.real,cmap='gray')
	f.savefig('bajas.png')
else:
	m,n,IF_high = F2(FI_high, True)
	ax.imshow(IF_high.real,cmap='gray')
	f.savefig('altas.png')