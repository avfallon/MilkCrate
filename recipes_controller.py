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

	def open_recipe_page(self, recipe_name):
		recipe = model.get_recipe(recipe_name)
		return recipe.recipe_info
		# accesses information from model for that recipe
		# calls view function to open recipe page w/ that info

	def open_edit_page(self, recipe_name):
		pass
		# access recipe information from model
		# call view function to open edit page

	def open_home_page(self):
		pass
		# call view function to open home page

	def open_new_recipe_page(self):
		#empty recipe page
		pass

	def make_recipe_list(self):
		return [{'text': recipe_name} for recipe_name in model.recipe_dict]