from kivy.app import App
# from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.listview import ListItemButton
from kivy.uix.screenmanager import ScreenManager, Screen

# RecycleView stuff
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.popup import Popup


from model_w_recipe import *
model = RecipeBook("andrew", "password", "localhost", "recipes", "recipes", "ingredients", "recipe_name")


# RecycleView stuff
class RecycleViewRow(BoxLayout):
    text = StringProperty()

    def go_to_rec(self, recipe_name):
	    print(recipe_name)






class HomeScreen(Screen):
	recipe_list = ObjectProperty()

	def tester(self):
		print("Test complete")

	def populate_recipe_list(self, category, value):
		search_dictionary = {value: category}
		name_list = model.filter_recipes(search_dictionary)
		for recipe in name_list:
			self.recipe_list.adapter.data.extend([recipe])
		self.recipe_list._trigger_reset_populate()

	pass


class RecipeViewScreen(Screen):
	pass


class MyScreenManager(ScreenManager):
	pass


class kivy_viewApp(App):
	def build(self):
		screen_manager = MyScreenManager()
		return screen_manager
		#return RecipeViewScreen()
		#return HomeScreen()




kivy_viewApp().run()
