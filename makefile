All: 
	make punto1
	make punto2
	make punto3

punto3:
	c++ 3_Fourier.cpp -o fourier
	./fourier datos.txt
	rm fourier

punto2:
	python 2_filtro.py chess.png altas
	python 2_filtro.py chess.png bajas

punto1:
	python 1_suave.py chess.png 20
	
