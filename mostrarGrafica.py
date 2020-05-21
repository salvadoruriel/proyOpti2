import networkx as nx
import networkx.generators.small as gs
import matplotlib.pyplot as plt

#g = gs.krackhardt_kite_graph()
#https://networkx.github.io/documentation/networkx-1.10/reference/generated/networkx.convert_matrix.from_numpy_matrix.html
def imprimeGraf(mat, numeroNodoInicial = 1, guardarImagen=0, dirigida=0):
	if(dirigida):
		g = nx.from_numpy_matrix(mat, create_using=nx.DiGraph())
	else:
		g = nx.from_numpy_matrix(mat)
	#ajustando nodos a representacion normal
	labeldict = {}
	for i in range(0, mat.shape[0]):
		labeldict[i] = i+numeroNodoInicial

	nx.draw(g,labels=labeldict, with_labels=True, 
		node_color='#ffFFff',edgecolors='#000000')
	plt.show()
	if(guardarImagen):
		plt.savefig('tmp.png')