from model_w_recipe import *
from Test import *
from kivy.event import EventDispatcher

class Controller(EventDispatcher):
	view = ObjectProperty(None)

	def __init__(self):
		self.model = RecipeBook("andrew", "password", "localhost", "recipes", "recipes", "ingredients", "recipe_name")
		self.view = View(self)
		self.view.run_app()

	# accesses information from model for that recipe
	# calls view function to open recipe page w/ that info
	def switch_recipe(self, name):
		recipe_info = self.get_recipe_info(name)
		self.view.app.recipeView.fill_recipe(recipe_info)

	def get_recipe_list(self):
		return self.model.recipe_dict

	def get_recipe_info(self, name):
		recipe = self.model.get_recipe(name)
		if recipe == None:
			return None
		else:
			return recipe.recipe_info


	def save_recipe(self, recipe_id, recipe_info):
		save_result = True
		if recipe_id == "":
			save_result = self.model.add_recipe(recipe_info)
		else:
			save_result = self.model.edit_recipe(recipe_id, recipe_info)
		#Eventually change to popup FIXME
		return save_result

	def delete_recipe(self, recipe_name):
		return self.model.delete_recipe(recipe_name)

class Main:
	def __init__(self):
		controller = Controller()



Main()