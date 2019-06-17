from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.properties import ObjectProperty
from kivy.uix.listview import ListItemButton

class RecipeListButton(ListItemButton):
	#return RecipeViewScreen
	pass

class RecipeDB():

	def add_recipe(self):
		pass
	pass

class HomeScreen(BoxLayout):

	recipe_list = ObjectProperty()
	pass


class RecipeViewScreen(BoxLayout):
	pass


class kivy_viewApp(App):
	def build(self):
		#return RecipeViewScreen()
		return HomeScreen()




kivy_viewApp().run()
