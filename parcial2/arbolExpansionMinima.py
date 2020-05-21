#python -m pip install numpy networkx matplotlib
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
mg = 999 #para caminos no posible como m grande
Eje1Midwest = np.array([
	[-1,1,5,7,9,mg],
	[0,-1,6,4,3,mg],
	[0,0,-1,5,mg,10],
	[0,0,0,-1,8,3],
	[0,0,0,0,-1,mg],
	[0,0,0,0,0,-1],
	])
#print(Eje1Midwest)
Eje1Midwest += np.triu(Eje1Midwest).transpose()
#print(Eje1Midwest)

def arbolExpMin(mat, nodoInicio= 0):
	#inicio en primer nodo
	vecIncl = [nodoInicio]
	#siempre es cuadrada aqui
	vecExcl = list(range(0, mat.shape[0]))
	vecExcl.remove(nodoInicio)

	mataux = np.zeros(shape = mat.shape) #matriz auxiliar de conexiones
	min=mg
	node=nodoInicio
	costo= 0
	#busco conexiones posibles la menor
	for idx,val in enumerate (mat[nodoInicio]):
		#evito que ya este el mismo nodo, o conexiones imposibles
		if(idx in vecIncl or val <= 0):
			continue
		if(val < min):
			min = val
			node= idx
	costo+=min

	#min = np.argmin(mat[nodoInicio])
	vecExcl.remove(node)
	#anexo conexion
	vecIncl.append(node)
	mataux[nodoInicio][node] = 1

	#repito
	return arbolExpMinRecur(mat, mataux, costo, vecIncl, vecExcl)


def arbolExpMinRecur(mat, mataux, costo, vecIncl, vecExcl):
	print(mat, '\n',mataux, costo, vecIncl, vecExcl)
	#print(costo, vecIncl, vecExcl)
	#return costo, vecIncl

	min=mg
	nodoIda=0
	#busco conexiones posibles la menor
	for nodoActual in vecIncl:
		for idx,val in enumerate (mat[nodoActual]):
			#evito que ya este el mismo nodo, o conexiones imposibles
			if(idx in vecIncl or val <= 0):
				continue
			if(val < min):
				min = val
				node= idx
				nodoIda= nodoActual
	costo+=min

	#min = np.argmin(mat[nodoInicio])
	vecExcl.remove(node)
	#anexo conexion
	vecIncl.append(node)
	mataux[nodoIda][node] = 1

	#si vecExcl es vacio, entonces repito
	if vecExcl:
		return arbolExpMinRecur(mat, mataux, costo, vecIncl, vecExcl)
	#regreso al final la conexion y su costo
	return costo, mataux

#########################################################
#PRUEBAS TEST
imprimeGraf(Eje1Midwest)
costo, mataux = arbolExpMin(Eje1Midwest,0)
print(costo)
imprimeGraf(mataux)