from model_w_recipe import *

model = RecipeBook("andrew", "password", "localhost", "recipes", "recipes", "ingredients", "recipe_name")

class Controller:
	def get_recipe_list():
		return model.recipe_dict

	def get_recipe_info(name):
		recipe = model.get_recipe(name)
		return recipe.recipe_info
	# accesses information from model for that recipe
	# calls view function to open recipe page w/ that info

