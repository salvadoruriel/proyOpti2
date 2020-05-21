#por floyd
import numpy as np
#importando la funcion para imprimir
if __name__ == '__main__':
    if __package__ is None:
        import sys
        from os import path
        sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
        from mostrarGrafica import imprimeGraf
    else:
        from ..mostrarGrafica import imprimeGraf

im = -1 #imposibles como caminos asi mismo
mg = 9999 #para caminos no posible como m grande
prob3Floyd = np.array([
	[-1,700,200,mg,mg,mg],
	[700,-1,300,200,mg,400],
	[200,300,-1,700,600,mg],
	[mg,200,700,-1,300,100],
	[mg,mg,600,300,-1,500],
	[mg,400,mg,100,500,-1]
	])
prob2Floyd = np.array([
	[-1,5,3,mg,mg,mg,mg],
	[5,-1,1,5,2,mg,mg],
	[3,1,-1,7,mg,mg,12],
	[mg,5,7,-1,3,mg,3],
	[mg,2,mg,3,-1,1,mg],
	[mg,mg,mg,1,1,-1,mg],
	[mg,mg,12,3,mg,4,-1]
	])
	

def rutaFloyd(mat, nodoInicio= 0, nodoDestino=1):

	matcopia = mat
	#matriz auxiliar de rutas
	mataux = np.zeros(shape = mat.shape).astype(int)
	for row in range(0,mataux.shape[0]):
		for col,val in enumerate (mataux[row]):
			#evitando mismo nodo
			if(row == col):
				mataux[row][col] = -1
			else:
				mataux[row][col] = col
	
	#haciendo tablas de floyd
	for k in range(0,mataux.shape[0]):
		#por cada renglon
		#print(k,matcopia,'\n',mataux)
		for row in range(0,mataux.shape[0]):
			if(row == k): continue
			#por cada columna
			for col,val in enumerate (mataux[row]):
				#evitando mismo nodo
				if(col == k or row == col):
					continue
				suma=matcopia[row][k] + matcopia[k][col]
				if(suma < matcopia[row][col]):
					#tabla escalas
					mataux[row][col] = k
					#tabla valores
					matcopia[row][col] = suma
	
	matcamino=np.zeros(shape = mat.shape)

	#busco camino recursivamente
	matcamino = buscaCamino(mat, mataux, matcamino, nodoInicio, nodoDestino)

	costo=matcopia[nodoInicio][nodoDestino]
	#termino
	return matcamino, matcopia, mataux, costo

def buscaCamino(mat, mataux, matcamino, nodoInicio, nodoDestino):
	#print(matcamino, nodoInicio,nodoDestino)
	temp = mataux[nodoInicio][nodoDestino]
	#checo si del nodo ya voy directamente a mi destino
	if(temp != nodoDestino):
		#si no, examino ese camino hasta la ruta directa
		buscaCamino(mat, mataux, matcamino, temp, nodoDestino)
		#recursivamente para del inicio al temporal tambien
		buscaCamino(mat, mataux, matcamino, nodoInicio, temp)
	else:
		#marco camino y costo, del inicio al destino
		matcamino[nodoInicio][nodoDestino] = mat[nodoInicio][nodoDestino]

	#ya llegue
	return matcamino


#########################################################
#PRUEBAS TEST
prob=prob2Floyd
#imprimeGraf(prob)
camino, a, b, costo = rutaFloyd(prob, nodoInicio=0, nodoDestino=6, )
print(costo, camino)
imprimeGraf(camino, dirigida=1)
