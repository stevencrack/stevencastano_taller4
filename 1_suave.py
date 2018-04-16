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
M,N = np.shape(I)

ancho = float(argv[2])
# Crear Filtro
t = np.arange(-ancho,ancho)/ancho
m,n = np.meshgrid(t,t)
r = (m**2+n**2)**0.5
k = np.exp(-ancho/2*r**2)

K = np.ones((M,N), dtype=float)*0
for i in range(M):
    for j in range(N):
        if i<np.size(k,0) and j<np.size(k,1):
            K[i,j] = k[i,j]
        else: 
            K[i,j] = 0.0

# transformada del filtro
m,n,KFT = F2(K,inv=False)

# Aplicar Filtro
FI_gauss = KFT*FI2

# Devolver a imagen
m,n,imagen = F2(FI_gauss, inv=True)

# Gaurdar imagen
f,ax = plt.subplots()
ax.imshow(imagen.real, cmap='gray')
f.savefig('suave.png')