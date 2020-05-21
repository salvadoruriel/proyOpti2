from os.path import dirname, join

from kivy.app import App
from kivy.lang import Builder #para cargar screens
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, StringProperty, BooleanProperty,\
    ListProperty
from kivy.animation import Animation
from kivy.uix.screenmanager import Screen

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
            'Inicio', 'Parcial_1', 'Parcial_2', 'Parcial_3',
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


if __name__ == '__main__':
    MenuApp().run()