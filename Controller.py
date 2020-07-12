from RecipeModel import *
from KivyView import *
from kivy.event import EventDispatcher


NEW_ID = "#*$&^#*($&#"

class Controller(EventDispatcher):
    view = ObjectProperty(None)

    def __init__(self):
        self.model = RecipeBook("andrew", "password", "localhost", "recipes",
                                "recipes", "ingredients", "recipe_name")
        self.view = View(self)
        self.view.run_app()

    # accesses information from model for that recipe
    # calls view function to open recipe page w/ that info
    def switch_recipe(self, name):
        recipe_info = self.get_recipe_info(name)
        self.view.app.recipeView.fill_recipe(recipe_info)

    def get_recipe_info(self, name):
        recipe = self.model.get_recipe(name)
        if recipe is None:
            return None
        else:
            return recipe.recipe_info

    # category_dict says which recipes to return, either all of them (home),
    # all the recipes in a particular category {upper_level:lower_level),
    # or the low level category options for a high level category (value of "")
    def get_recipe_list(self, category_dict):
        return self.model.filter_recipes(category_dict)

    # Save a recipe, either a new one or an edit of an existing recipe
    def save_recipe(self, recipe_id, recipe_info):
        save_result = True
        if recipe_id == NEW_ID:
            save_result = self.model.add_recipe(recipe_info)
        else:
            save_result = self.model.edit_recipe(recipe_id, recipe_info)
        # Eventually change to popup instead of just printing FIXME
        return save_result

    # Delete a recipe from the database, called by view
    def delete_recipe(self, recipe_name):
        return self.model.delete_recipe(recipe_name)

    # Return the lower level values of a specified upper level category
    def get_category_list(self, upper_cat):
        return self.model.get_category_values(upper_cat)


class Main:
    def __init__(self):
        Controller()


Main()
