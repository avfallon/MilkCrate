from model_w_recipe import *
from Test import *



class Controller:
	def __init__(self):

		self.current_recipe_name = ""
		self.current_recipe_info = {}


	def save_new_recipe(self, col1, col2, col3, col4, col5, col6, col7, col8):
		pass
		# Takes in all values entered into text boxes, these will be the recipe information
			# Going to have to be a limit on how many categories,
			# if there are less, just pass blank, this function won't process them

		# updates model with arguments
		# This function ends, but the view function that calls it will then open that new recipe's page

	def get_recipe_info(self, recipe_name, model):
		recipe = self.model.get_recipe(recipe_name)
		self.current_recipe_name = recipe_name
		self.current_recipe_info = recipe.recipe_info
		return self.current_recipe_info
		# accesses information from model for that recipe
		# calls view function to open recipe page w/ that info

	def open_recipe_page(self):
		pass


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

	# Returns a list of all recipe bodies in the database
	def make_recipe_list(self):
		return [{'text': recipe_name} for recipe_name in model.recipe_dict]

def Main(self):
	self.controller = Controller()
	model = RecipeBook("andrew", "password", "localhost", "recipes", "recipes", "ingredients", "recipe_name")

	# Instantiate the view, fill recipes to main home screen, the opener
	while(1):
		# Receive message from the view, what has just been pressed
		# Get either new recipe list or the recipe info for that click
		# call function in view that A) switches to recipe screen and fills the info
		# B) changes to a new category screen
		# C) changes to edit recipe

		# clock on recipe to view
		# recipe to edit
		# category to category screen
		# search
		# back
		# settings


