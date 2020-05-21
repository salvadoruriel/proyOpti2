#(23/03/2020) hace en forma de matriz
#con 4 matrices, primal d

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

ini= -5 #valor de nodo antes del que se inicia
mg = 9999 #para caminos no posible como m grande
#problema con valor del mismo nodo como bi
#sin restricciones desbalanceado
prob9_4 = np.array([
	[4, 1,3,0],
	[0,-1,0,4],
	[0,-2,2,3],
	[0,0,0,-4]
	])
#sin restricciones balanceado
probEjemplo = np.array([
	[4, 2,-5,0],
	[0, 2,6,4],
	[0,-1,-1,3],
	[7,0,0,-5]
	])
#sin limites
sinFlujoMin = np.array([
	[0,0,0,0],
	[0,0,0,0],
	[0,0,0,0],
	[0,0,0,0]
	])
sinFlujoMax = np.array([
	[mg,mg,mg,mg],
	[mg,mg,mg,mg],
	[mg,mg,mg,mg],
	[mg,mg,mg,mg]
	])

def simplexRedes(mat, matFlujoMin, matFlujoMax, iter=999):
	#verificar que esta balanceado
	sum=0
	for node in range(0,mat.shape[0]):
		sum += mat[node][node]
		
	if(sum == 0):
		#creo nodo artificial y hago conexiones
		#np pat(mat, ((arriba,abajo),(izq, der)), etc.
		solFacInicial = np.pad(mat, ((0,1),(0,1)), mode='constant', constant_values=0)
		ultNodo = solFacInicial.shape[0] -1

		matprimal= np.zeros(shape = solFacInicial.shape)
		for nodo in range(0,mat.shape[0]):
			#conexion M que va del nodo artificial a los otros
			if(mat[nodo][nodo] <0):
				solFacInicial[ultNodo][nodo] = mg
				matprimal[ultNodo][nodo] = -1*mat[nodo][nodo]
			#al reves
			else:
				solFacInicial[nodo][ultNodo] = mg
				matprimal[nodo][ultNodo] = mat[nodo][nodo]
				
	#print(matprimal,solFacInicial)
	#return matprimal
	matprimal = pasoSimplex(solFacInicial, matprimal, 0, iter)
	#print(matprimal)
	return matprimal

def pasoSimplex(mat, matprimal,iter=0, maxiter=999):
	print(iter,'matriz primal:\n', matprimal)

	#checando si se ha eliminado nodo auxiliar
	nodaux=0
	ultNodo = matprimal.shape[0]-1
	for row in range(0,matprimal.shape[0]):
		nodaux += matprimal[row][ultNodo] + matprimal[ultNodo][row]
	if(nodaux == 0):
		return matprimal[:-1,:-1]
			

	#calculo dual
	vecCostoDual = [np.nan] * mat.shape[0]
	#dual de nodo auxiliar es 0 siempre
	vecCostoDual[matprimal.shape[0] - 1] = 0
	while( np.nan in vecCostoDual ):
		for row in range(0,matprimal.shape[0]):
			for col,val in enumerate (matprimal[row]):
				#dual sobre rutas posibles
				if(val > 0):
					#busco ruta y agrego costo dual del nodo
					#si ambos nodos aun no tienen precio continuo hasta tenerlo
					if(np.isnan(vecCostoDual[col]) and np.isnan(vecCostoDual[row])):
						continue
					if(np.isnan(vecCostoDual[row])):
						# w_ini = w_des + costoruta_ini_dest
						vecCostoDual[row] = vecCostoDual[col] + mat[row][col]
					#asegurando no sobrescribir nodos ya hecho
					elif(np.isnan(vecCostoDual[col])):
						# w_des = w_ini - costoruta_ini_dest
						vecCostoDual[col] = vecCostoDual[row] - mat[row][col]
	
	#calculo sombra
	matPrecioSombra = np.full(shape = matprimal.shape, fill_value=np.nan)
	max=0
	pivoteini = -1
	pivotedes = -1
	for row in range(0,mat.shape[0]):
		for col,val in enumerate (mat[row]):
			#precio sombra en rutas posibles (fantasma)
			#hago para rutas que estan en el fantasma pero no en primal
			if(matprimal[row][col]== 0 and mat[row][col] != 0 and row!=col ):
				#calculo precio sombra de la ruta guardando el menor a la vez
				#z12 -c12 = w_ini - w_des - c_ida_des
				matPrecioSombra[row][col]= vecCostoDual[row] - vecCostoDual[col] - mat[row][col]
				temp = matPrecioSombra[row][col]
				if(temp > max):
					max = temp
					pivoteini = row
					pivotedes = col
	np.set_printoptions(suppress=True)
	print(iter,'matriz Precio sombra y costo dual: \n',matPrecioSombra, vecCostoDual)
	if(max <= 0 or iter == maxiter):
		return matprimal

	#busca ciclo
	#	todas las rutas en el primal
	matcicloaux = matprimal + matprimal.transpose()
	matcicloaux[pivoteini][pivotedes]= 1
	# auxiliar par marcar ruta
	matcicloruta = np.zeros(matprimal.shape)
	matcicloruta[pivoteini][pivotedes] = 1
	#matcicloruta[pivotedes][pivoteini] = 1

	vecvisi = [pivotedes]
	matruta = buscaciclo(matcicloaux, matcicloruta, pivoteini, pivotedes, vecvisi)
	print(iter,'matriz de ciclo: \n',matruta)
	#matciclo = np.copy(matruta)

	#marca direccion
	for row in range(0,matprimal.shape[0]):
		for col,val in enumerate (matprimal[row]):
			#como solo hay 1 camino, el otro de ida/venida lo elimino
			if(matruta[row][col] == 1):
				if(matprimal[row][col] >0):
					matruta[col][row] = 0
				#si no, el camino contrario es el real
				else:
					matruta[col][row] = 1
					matruta[row][col] = 0
	print(iter,'caminos a pivotear:','\n',matruta)

	#busca menor a restar
		#dir = 1, direccion, 1 es de ida osea suma el pivote
	valPivote = buscaEnDireccion(pivoteini ,matprimal, matruta, pivoteini, pivotedes, mg, 1)
	#si ya no hay cambios significativos, osea solo tenemos bucles
	if(valPivote == 0):
		return matprimal

	#pivote resta y/o suma para una nueva matriz primal
	#print(matprimal)
	matprimal[pivoteini][pivotedes] = valPivote
	#print(matprimal)
	#vecvisi = [pivoteini, pivotedes]
	matprimal = cambiaPrimal(pivoteini, matprimal, matruta, pivoteini, pivotedes, valPivote, 1)

	iter += 1
	return pasoSimplex(mat, matprimal, iter, maxiter=maxiter)

############### FUNCIONES DEL METODO #############
def buscaciclo(mat, matruta, nodoIni, nodoDes, vecvisi):
	#print(mat)
	#print(matruta, vecvisi, nodoIni, nodoDes, nodoIni == nodoDes)
	if(nodoDes == nodoIni):
		return matruta
	for col,val in enumerate (mat[nodoDes]):
		#evitando vectores visitados
		if(col in vecvisi or col == nodoDes):
			continue
		#siguiendo camino
		if(val > 0):
			matruta[nodoDes][col] = 1
			vecvisi.append(col)
			temp = buscaciclo(mat, matruta, nodoIni, col, vecvisi) 
			if(temp is not None):
				return temp
			vecvisi.remove(col)
			matruta[nodoDes][col] = 0


def buscaEnDireccion(nodoAnt, mat, matruta, nodoIni, nodoDes, min, dir):
	if(nodoDes == nodoIni):
		return min
	print('buscando: ',min, nodoAnt, nodoDes, dir)
	#en direccion de ida, positiva al pivote
	if(dir == 1):
		for col,val in enumerate(matruta[nodoDes]):
			if(col == nodoAnt): continue
			if(val > 0):
				nodoAnt= nodoDes
				return buscaEnDireccion(nodoAnt, mat,matruta,nodoIni, col, min, dir)
		#no sigue derecho, cambia la direccion con pivote negativo
		dir = -1
		for row in range(0,matruta.shape[0]):
			if(row == nodoAnt): continue
			val = mat[row][nodoDes]
			if(val > 0 and matruta[row][nodoDes] > 0):
				if(val < min):
					#print(min,val,nodoAnt, nodoDes)
					min = val
				nodoAnt= nodoDes
				return buscaEnDireccion(nodoAnt,mat,matruta,nodoIni, row, min, dir)
	#debo ir en direccion contraria al pivote
	else:
		for row in range(0,matruta.shape[0]):
			if(row == nodoAnt): continue
			val = mat[row][nodoDes]
			if(val > 0 and matruta[row][nodoDes] > 0):
				if(val < min):
					#print(min,val,nodoAnt, nodoDes)
					min = val
				nodoAnt= nodoDes
				return buscaEnDireccion(nodoAnt,mat,matruta,nodoIni, row, min, dir)
		#cambia otra vez la direccion,
		dir=1
		for col,val in enumerate(matruta[nodoDes]):
			if(col == nodoAnt): continue
			if(val > 0):
				nodoAnt= nodoDes
				return buscaEnDireccion(nodoAnt,mat,matruta,nodoIni, col, min, dir)

	
def cambiaPrimal(nodoAnt, matprimal, matruta, nodoIni, nodoDes, valpiv,dir):
	if(nodoDes == nodoIni):
		return matprimal
	#en direccion de ida, positiva al pivote
	#print(nodoAnt, nodoDes, valpiv, matruta, dir)
	if(dir == 1):
		for col,val in enumerate(matruta[nodoDes]):
			#evitando regresar por mismo camino
			#if(col in vecvisi): continue
			if(col == nodoAnt): continue
			if(val > 0):
				#vecvisi.append(col)
				nodoAnt = nodoDes
				matprimal[nodoDes][col] += valpiv
				return cambiaPrimal(nodoAnt, matprimal, matruta,nodoIni, col, valpiv, dir)
		#no sigue derecho, cambia la direccion con pivote negativo
		dir = -1
		for row in range(0,matruta.shape[0]):
			#if(row in vecvisi): continue
			if(row == nodoAnt): continue
			val = matruta[row][nodoDes]
			#if(row==nodoIni): continue
			if(val > 0):
				#vecvisi.append(row)
				nodoAnt = nodoDes
				matprimal[row][nodoDes] -= valpiv
				return cambiaPrimal(nodoAnt, matprimal, matruta,nodoIni, row, valpiv, dir)
		print('no deberia llegar aqui: ', )
	#debo ir en direccion contraria al pivote
	else:
		for row in range(0,matruta.shape[0]):
			#if(row in vecvisi): continue
			if(row == nodoAnt): continue
			val = matruta[row][nodoDes]
			if(val > 0):
				#vecvisi.append(col)
				nodoAnt = nodoDes
				matprimal[row][nodoDes] -= valpiv
				return cambiaPrimal(nodoAnt, matprimal, matruta,nodoIni, row, valpiv, dir)
		#cambia otra vez la direccion,
		dir=1
		for col,val in enumerate(matruta[nodoDes]):
			#if(col in vecvisi): continue
			if(col == nodoAnt): continue
			if(val > 0):
				#vecvisi.append(row)
				nodoAnt = nodoDes
				matprimal[nodoDes][col] += valpiv
				return cambiaPrimal(nodoAnt, matprimal, matruta,nodoIni, col, valpiv, dir)

#########################################################
#PRUEBAS TEST
prob=probEjemplo
#imprimeGraf(prob)
matriz = simplexRedes(prob, sinFlujoMin, sinFlujoMax, iter=3)
print(matriz)
imprimeGraf(matriz, dirigida=1)
