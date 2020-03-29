

class Controller:
	def __init__(self):

		self.current_recipe_name = ""
		self.current_recipe_info = {}

	def instantiate(self, view, model):
		self.view = view
		self.model = model

	def save_new_recipe(self, col1, col2, col3, col4, col5, col6, col7, col8):
		pass
		# Takes in all values entered into text boxes, these will be the recipe information
			# Going to have to be a limit on how many categories,
			# if there are less, just pass blank, this function won't process them

		# updates model with arguments
		# This function ends, but the view function that calls it will then open that new recipe's page

	def get_recipe_info(self, recipe_name):
		recipe = self.model.get_recipe(recipe_name)
		self.current_recipe_name = recipe_name
		self.current_recipe_info = recipe.recipe_info
		return self.current_recipe_info
		# accesses information from model for that recipe
		# calls view function to open recipe page w/ that info


class Main:
	def __init__(self):
		controller = Controller()
		view = View(controller)
		#model = RecipeBook("andrew", "password", "localhost", "recipes", "recipes", "ingredients", "recipe_name")
		#controller.instantiate(view, model)


	#  fill recipes to main home screen, the opener
	#while(1):
		#pass
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


Main()