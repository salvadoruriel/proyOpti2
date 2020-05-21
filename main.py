from os.path import dirname, join

from kivy.app import App
from kivy.lang import Builder #para cargar screens
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, StringProperty, BooleanProperty,\
		ListProperty
from kivy.animation import Animation
from kivy.uix.screenmanager import Screen

import numpy as np
from mostrarGrafica import imprimeGraf
from parcial2.arbolExpansionMinima import *

mg = 99999

#Basado en ShowcaseScreen
class ContentScreen(Screen):
		fullscreen = BooleanProperty(False)

		def add_widget(self, *args):
				if 'content' in self.ids:
						return self.ids.content.add_widget(*args)
				return super(ContentScreen, self).add_widget(*args)

#MAIN
class MenuApp(App):

		index = NumericProperty(-1)
		current_title = StringProperty()
		screen_names = ListProperty([])
		#i shouldn't need these
		time = NumericProperty(0)
		hierarchy = ListProperty([])

		def build(self):
				self.title = 'Optimizacion 2 Solver'
				self.screens = {} #pantallas cargadas
				self.screen_names =sorted([
						'0 Inicio', 'Parcial_1', '2 Arbol de expansion minima', 'Parcial_3',
						'xyz'])
				self.available_screens = [join(dirname(__file__), 'pantallas',
						'{}.kv'.format(fn).lower()) for fn in self.screen_names]
				self.go_screen(0) #ir a 1er pantalla
				#return ContentScreen()

		def on_pause(self):
				return True

		def on_resume(self):
				pass

		def on_current_title(self, instance, value):
				self.root.ids.spnr.text = value

		def go_screen(self, idx):
				self.index = idx
				self.root.ids.sm.switch_to(self.load_screen(idx), direction='left')
				self.current_title = self.screens[idx].name

		#busca pantalla cargada, sino, carga el archivo y la pantalla
		def load_screen(self, index):
				if index in self.screens:
						return self.screens[index]
				screen = Builder.load_file(self.available_screens[index])
				self.screens[index] = screen
				return screen

		######funciones de algunas pantallas ######
		######
		def muestra_grid(self, layout, nodosInput, dirigida=0):
				if not layout.get_parent_window():
						return
				nodos = int(nodosInput.text)
				if(not isinstance(nodos, int) or nodos <= 0):
					print('no es un numero valido')
					return
				layout.clear_widgets()
				layout.cols = nodos
				layout.rows = nodos
				#haciendo matriz cuadrada
				for row in range(0,nodos):
					for col in range(0,nodos):
						#el contenido toma en cuenta los espacios
						#si no es dirigida(0) solo habilito los de ida
						if(dirigida):
							layout.add_widget(Builder.load_string(
'''
TextInput:
	id: '{}{}'.format(row,col)
	text: '0'
	multiline: False
	size_hint_y: None
	height: '32dp'
	size_hint_x: None
	width: '54dp'
	disabled: False
'''
							))
						elif(col >= row):
							layout.add_widget(Builder.load_string(
'''
TextInput:
	id: '{}{}'.format(row,col)
	text: '0'
	multiline: False
	size_hint_y: None
	height: '32dp'
	size_hint_x: None
	width: '54dp'
	disabled: False
'''
							))
						else:
							layout.add_widget(Builder.load_string(
'''
TextInput:
	id: '{}{}'.format(row,col)
	text: '0'
	multiline: False
	size_hint_y: None
	height: '32dp'
	size_hint_x: None
	width: '54dp'
	disabled: True
'''
							))

				print('matriz lista')
		
		def resuelve_arbolmin(self, layout, nodosInput, costoLabel, layoutRes):
				if not layout.get_parent_window():
						return
				nodos = int(nodosInput.text)
				if(not isinstance(nodos, int) or nodos <= 0):
					print('no es un numero valido')
					return
				matrizProblema = np.zeros( shape= (nodos,nodos) )
				'''
				for row in range(0,nodos):
					for col in range(0,nodos):
						#matrizProblema[row][col] = ('{}{}'.format(row,col))[row][col]
						#lrow acomodo de renglon en layout
						lrow = row +nodos-1 %(nodos)
						temp = layout.children[ row*nodos + col].text
						print(row,col ,layout.children[ row*nodos + col].text)
						#temp = 'self.ids.{}{}.text'.format(row,col)
						if(temp == 'M' or temp == 'm' or temp=='mg'):
							matrizProblema[row][col] = mg
						else:
							matrizProblema[row][col] = int(temp)
				'''
				row=0
				col=0
				for tempnod in reversed(layout.children):
					temp = tempnod.text
					if(temp == 'M' or temp == 'm' or temp=='mg'):
						matrizProblema[row][col] = mg
					else:
						matrizProblema[row][col] = int(temp)
					col += 1
					if(col >= nodos):
						col = 0
						row += 1

				#convierto dirigida en no dirigida
				matrizProblema = matrizProblema + matrizProblema.transpose()
				#resuelve
				costo,mataux = arbolExpMin(matrizProblema,0)
				#print(mataux)
				#coloca resultado
				costoLabel.text = 'costo: {}'.format(costo)
				imprimeGraf(mataux)




if __name__ == '__main__':
		MenuApp().run()