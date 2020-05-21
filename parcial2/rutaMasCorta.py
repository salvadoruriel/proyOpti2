#por dijkstra
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
ini= -5 #valor de nodo antes del que se inicia
mg = 99999 #para caminos no posible como m grande
#creo no tuve el planteamiento completo de este
prob3 = np.array([
	[-1,1700,3968,7370,10286],
	[mg,-1,1880,4652,7028],
	[mg,mg,-1,2300,4316],
	[mg,mg,mg,-1,2720],
	[mg,mg,mg,mg,-1]
	])
prob2b = np.array([
	[-1,5,1,mg,mg,mg,mg],
	[mg,-1,mg,7,1,6,mg],
	[mg,2,-1,6,7,mg,mg],
	[mg,mg,7,-1,mg,4,6],
	[mg,mg,mg,3,-1,5,9],
	[mg,7,mg,mg,mg,-1,2],
	[mg,mg,mg,mg,mg,mg,-1]
	])


def rutaDijkstra(mat, nodoInicio= 0, nodoDestino=1):
	np.set_printoptions(suppress=True)
	if(nodoDestino >= mat.shape[0]):
		print('error: nododestino fuera de tamaño de matriz')
		return np.zeros(shape = mat.shape), 0, 0
	#inicio en primer nodo
	vecPerm = [nodoInicio]
	#etiquetas, todas con indice correspondiente a nodo
	#etiquetas de que nodo llega a ese
	vecEtiqIda = [-1]*mat.shape[0]
	#etiquetas de costo más bajo
	vecEtiqCosto = [mg]* mat.shape[0]

	#inicio en el nodo marcado
	vecPerm.append(nodoInicio)
	vecEtiqIda[nodoInicio] = ini
	vecEtiqCosto[nodoInicio] = 0
	
	while( not(nodoInicio in vecPerm and nodoDestino in vecPerm) ):
		#busco conexiones posibles la menor
		minglobal = mg
		node=-1
		nodoIda=-1
		for row in vecPerm:
			for col,val in enumerate (mat[row]):
				min = vecEtiqCosto[col]
				val += vecEtiqCosto[row]
				#evito permanentes o rutas imposibles
				if(col in vecPerm or val <= 0):
					continue
				#ajusto etiquetas y la ruta de ida
				if(val < min):
					vecEtiqCosto[col] = val
					vecEtiqIda[col] = row
				if(val < minglobal):
					minglobal= val
					node= col
					nodoIda = row
		vecPerm.append(node)

	matcamino = np.zeros(shape = mat.shape) #matriz auxiliar de camino
	#recursivamente busco el camino desde el fin al inicio
	matcamino= marcaCamino(mat, matcamino, vecEtiqCosto, vecEtiqIda, nodoDestino)
	costo = vecEtiqCosto[nodoDestino]
	#termine
	return matcamino, vecPerm, costo

def marcaCamino(mat, matcamino, vecEtiqCosto, vecEtiqIda, nodoDestino):
	nodoanterior = vecEtiqIda[nodoDestino]
	if(nodoanterior == ini):
		return matcamino
	#marco camino
	matcamino[nodoanterior][nodoDestino] = mat[nodoanterior][nodoDestino]
	#repito buscando camino al nodo ultimo
	nodoDestino=nodoanterior
	return marcaCamino(mat, matcamino, vecEtiqCosto, vecEtiqIda, nodoDestino)


#########################################################
#PRUEBAS TEST
prob=prob2b
#imprimeGraf(prob)
camino, vecPerm, costo = rutaDijkstra(prob, nodoInicio=0, nodoDestino=4, )
print(costo, camino)
imprimeGraf(camino, dirigida=1)
