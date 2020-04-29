from kivy.app import App
from kivy.properties import BooleanProperty, ObjectProperty
from kivy.properties import NumericProperty
from kivy.uix.textinput import TextInput
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.label import Label
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.screenmanager import ScreenManager, Screen


# RecycleView stuff
class CustomScreen(Screen):
    hue = NumericProperty(0)


class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    ''' Adds selection and focus behaviour to the view. '''


class SelectableLabel(RecycleDataViewBehavior, Label):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    """ Add selection support to the Label """
    index = None

    def refresh_view_attrs(self, rv, index, data):
        """ Catch and handle the view changes """
        self.index = index
        return super(SelectableLabel, self).refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def on_press(self):
        self.selected = True

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        if is_selected:
            # opens the page associated with that recipe name
            recipe_name = rv.data[index]["text"]
            rv.controller.switch_recipe(recipe_name)
            rv.manager.current = "recipeView"

    def on_release(self, rv, index, is_selected):
        print(rv.data[index])


class RV(RecycleView):
    manager = ObjectProperty(None)
    controller = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)

    def update(self):
        self.data = [{'text': key} for key in self.controller.get_recipe_list()]

class RVScreen(Screen):
    pass

class CategoryLabel(Label):
    pass

class CategoryInput(TextInput):
    pass

class HomeScreen(Screen):
    controller = ObjectProperty(None)
    app = ObjectProperty(None)

    def new_recipe(self):
        self.app.editRecipe.new_recipe()
        self.manager.current = "editRecipe"


class RecipeViewScreen(Screen):
    controller = ObjectProperty(None)
    app = ObjectProperty(None)
    recipe_info = {}

    def fill_recipe(self, recipe_info):
        self.recipe_info = recipe_info
        self.ids.name.text = recipe_info["name"]
        self.ids.ingredients.text = recipe_info["ingredients"]
        self.ids.instructions.text = recipe_info["instructions"]
        self.ids.category.text = "Category: " + recipe_info["category"]
        self.ids.meal.text = "Meal: " + recipe_info["meal"]
        self.ids.ethnicity.text = "Ethnicity: " + recipe_info["ethnicity"]
        self.ids.difficulty.text = "Difficulty: " + recipe_info["difficulty"]
        self.ids.price.text = "Price: " + recipe_info["price"]
        self.ids.prep.text = "Prep Time: " + recipe_info["prep time"]

    def edit_recipe(self):
        self.app.editRecipe.fill_recipe(self.recipe_info)
        self.manager.current = "editRecipe"

class EditRecipeScreen(Screen):
    controller = ObjectProperty(None)
    app = ObjectProperty(None)
    NEW_ID = "#*$&^#*($&#"
    recipe_id = NEW_ID

    def fill_recipe(self, recipe_info):
        if recipe_info == None:
            print("Invalid recipe")
            self.manager.current = "home"
            return
        self.recipe_id = recipe_info["name"]
        self.ids.name.text = recipe_info["name"]
        self.ids.ingredients.text = recipe_info["ingredients"]
        self.ids.instructions.text = recipe_info["instructions"]
        self.ids.category.text = "Category: " + recipe_info["category"]
        self.ids.meal.text = "Meal: " + recipe_info["meal"]
        self.ids.ethnicity.text = "Ethnicity: " + recipe_info["ethnicity"]
        self.ids.difficulty.text = "Difficulty: " + recipe_info["difficulty"]
        self.ids.price.text = "Price: " + recipe_info["price"]
        self.ids.prep.text = "Prep Time: " + recipe_info["prep time"]

    def new_recipe(self):
        self.recipe_id = self.NEW_ID
        self.ids.name.text = ""
        self.ids.ingredients.text = ""
        self.ids.instructions.text = ""
        self.ids.category.text = "Category: "
        self.ids.meal.text = "Meal: "
        self.ids.ethnicity.text = "Ethnicity: "
        self.ids.difficulty.text = "Difficulty: "
        self.ids.price.text = "Price: "
        self.ids.prep.text = "Prep Time: "

    def save_recipe(self):
        new_info = {
            "name": self.ids.name.text,
            "ingredients": self.ids.ingredients.text,
            "instructions": self.ids.instructions.text,
            "category": self.ids.category.text[9:],
            "meal": self.ids.meal.text[5:],
            "prep time": self.ids.prep.text[10:],
            "difficulty": self.ids.difficulty.text[11:],
            "price": self.ids.price.text[6:],
            "ethnicity": self.ids.ethnicity.text[10:]}

        self.controller.save_recipe(self.recipe_id, new_info)

        self.app.home.rv.update()
        self.controller.switch_recipe(new_info["name"])
        self.manager.transition.direction = 'right'
        self.manager.current = "recipeView"

    def delete_recipe(self):
        if self.recipe_id == self.NEW_ID:
            self.manager.current = "home"
        else:
            self.controller.delete_recipe(self.recipe_id)
            self.app.home.rv.update()
            self.manager.current = "home"


class TestApp(App):
    manager = ObjectProperty(None)
    home = ObjectProperty(None)
    recipeView = ObjectProperty(None)
    editRecipe = ObjectProperty(None)
    controller = ObjectProperty(None)

    def build(self):
        self.manager = self.instantiate()
        return self.manager

    def instantiate(self):
        screen_man = ScreenManager()
        self.home = HomeScreen(name="home", controller=self.controller, app=self)
        self.recipeView = RecipeViewScreen(name="recipeView", controller=self.controller, app=self)
        self.editRecipe = EditRecipeScreen(name="editRecipe", controller=self.controller, app=self)
        screen_man.add_widget(self.home)
        screen_man.add_widget(self.recipeView)
        screen_man.add_widget(self.editRecipe)
        return screen_man

    # returns list of recipe names for recycleview instantiation
    def gen_rv_data(self):
        return [{'text': key} for key in self.controller.get_recipe_list()]


class View:
    def __init__(self, controller_in):
        self.app = TestApp()
        self.app.controller = controller_in

    # Separate run from init to allow view instantiation in controller, before running pauses everything
    def run_app(self):
        self.app.run()
