from model_w_recipe import *
from Test import *

#model = RecipeBook("andrew", "password", "localhost", "recipes", "recipes", "ingredients", "recipe_name")

class Controller:
	def get_recipe_list(self):
		return model.recipe_dict

	def switch_recipe(name):
		recipe_info = model.get_recipe(name).recipe_info


	def get_recipe_info(self, name):
		recipe = model.get_recipe(name)
		return recipe.recipe_info
	# accesses information from model for that recipe
	# calls view function to open recipe page w/ that info

class Main:
	def __init__(self):
		model = RecipeBook("andrew", "password", "localhost", "recipes", "recipes", "ingredients", "recipe_name")
		controller = Controller()
		view = View(controller)

Main()