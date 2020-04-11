from model_w_recipe import *

model = RecipeBook("andrew", "password", "localhost", "recipes", "recipes", "ingredients", "recipe_name")

class Controller:

	def save_new_recipe(self, col1, col2, col3, col4, col5, col6, col7, col8):
		pass
	# Takes in all values entered into text boxes, these will be the recipe information
		# Going to have to be a limit on how many categories,
		# if there are less, just pass blank, this function won't process them

	# updates model with arguments
	# This function ends, but the view function that calls it will then open that new recipe's page

	def get_recipe_info(name):
		recipe = model.get_recipe(name)
		return recipe.recipe_info
	# accesses information from model for that recipe
	# calls view function to open recipe page w/ that info


