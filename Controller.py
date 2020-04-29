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
		self.view.app.recipeView.update_recipe(recipe_info)

	def get_recipe_list(self):
		return self.model.recipe_dict

	def get_recipe_info(self, name):
		recipe = self.model.get_recipe(name)
		return recipe.recipe_info

	def new_recipe(self):
		self.view.app.editRecipe.title = ""
		self.view.app.editRecipe.ingredients = ""
		self.view.app.editRecipe.instructions = ""

		pass

	def edit_recipe(self):
		pass

class Main:
	def __init__(self):
		controller = Controller()



Main()