#include "stdio.h"
#include "stdlib.h"
#include "stdbool.h"
#include "math.h"


int main(int argc, char const *argv[])
{
	int i;
	char a_salida[20]="transformada.txt";
	printf("%s\n", argv[1]);

	int j;
	int n_lines;

	FILE *a_entrada; 
	a_entrada = fopen(argv[1], "r");

	int test;
	

	// Contar lineas
	n_lines = 0;
	do{
		i = fgetc(a_entrada);
		if(i=='\n'){
			n_lines++;
		}
	}while(i!=EOF);
	fclose(a_entrada); // cerrar archivo
	printf("%d\n", n_lines);


	int n;
	n = 7;
	float **D;
	D = malloc(n_lines*n*sizeof(float));
	for (i = 0; i < n; i++)
	{
		D[i] = malloc(n_lines*sizeof(float));
	}


	a_entrada = fopen(argv[1], "r"); // Volver a abrir archivo
	for (i = 0; i < n_lines; i++)
	{
		fscanf(a_entrada,"%f,%f\n", &D[0][i], &D[1][i]); // cargar datos en D
		for (j = 2; j < n; j++)
		{
			D[j][i] = 0.0; // Llenar los otros datos con ceros
		}

		//printf("%f,%f,%f,%f,%f,%f,%f\n",D[0][i],D[1][i],D[2][i],D[3][i],D[4][i],D[5][i],D[6][i]);
	}
	
	// D es una matriz de 7 columnas y n filas
	// col0 es t
	// col1 es y
	// col2 es para nuevo x
	// col3 es para nuevo y
	// col4 es para frecuencia
	// col5 es para parte real de la transformada
	// col6 es para nuevo imaginaria de la transformada



	int nmax = 20; // Maxima cantidad de numeros
	// para que Lagrange sea estable

	// Crear nuevo tiempo uniforme
	float t_tot;
	t_tot = (D[0][nmax-1]-D[0][0]); // tiempo total
	float dt;
	dt = t_tot/(nmax-1); // delta de tiempo

	D[2][0] = D[0][0]; // Tiempo inicial es el mismo
	for (i = 1; i < nmax; i++)
	{
		D[2][i] = D[2][i-1]+dt;
	}


	
	float lj;
	int k;
	float x;
	float xj;
	float yj;
	float L;
	for (i = 0; i < nmax; i++) // Seleccionar cada nuevo valor
	{
		x = D[2][i]; // x a interpolar
		L = 0.0;
		for (j = 0; j < nmax; ++j) // Sumatoria
		{
			yj = D[1][j];
			xj = D[0][j];
			lj = 1.0;

			for (k = 0; k < j; ++k) // Multiplicatoria menores a j
			{
				lj = lj*(x-D[0][k])/(xj-D[0][k]);
			}
			
			for (k = j+1; k < nmax; ++k) // Multiplicatoria mayores a j
			{
				lj = lj*(x-D[0][k])/(xj-D[0][k]);
			}
			L = L + yj*lj;
		}		

		D[3][i] = L;
	}


	float yn;
	for (k = 0; k < nmax; ++k)
	{
		for (i = 0; i < nmax; ++i)
		{
			yn = D[3][i];
			D[5][k] = D[5][k] + yn*cos(-6.28*k*i/nmax);
			D[6][k] = D[6][k] + yn*sin(-6.28*k*i/nmax);
			// i en la formula es solo para mostrar que es imaginario
			// En esta implementacion, la i corresponde a la n de la formula
		}
	}

	int i1;
	int i2;
	i1 = 0;
	i2 = 1;

	// Construir vector de frecuencias
	// Vector de frecuencias queda como
	// 0 df 2df ... fs/2 -fs/2+df ... -df
	float df;
	df = 1.0/(2.0*dt)*(1/((float)(nmax)/2));
	float fs;
	fs = 1.0/dt;

	D[4][0] = 0.0;
	
	for (k = 0; k < nmax/2-1; ++k)
	{
		D[4][i1+1] = D[4][i1] + df;

		if (k<nmax/2-1)
		{
			D[4][nmax/2+i2] = -fs/2 + i2*df;
			i2++;
		}
		i1++;
	}
	D[4][nmax/2] = -fs/2;

FILE *salida;
salida = fopen(a_salida,"w");
for (i = 0; i < nmax; ++i)
{
	//printf("%f,%f,%f,%f,%f,%f,%f\n",D[0][i],D[1][i],D[2][i],D[3][i],D[4][i],D[5][i],D[6][i]);
	fprintf(salida,"%f,%f,%f\n",D[4][i],D[5][i],D[6][i]);
}
fclose(salida);

	return 0;
}