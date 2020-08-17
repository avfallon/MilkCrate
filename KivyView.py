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
from kivy.uix.screenmanager import NoTransition
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.stacklayout import StackLayout


# RecycleView stuff
class CustomScreen(Screen):
    hue = NumericProperty(0)


class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    ''' Adds selection and focus behaviour to the view. '''
    # touch_deselect_last = BooleanProperty(True)


class RVLabel(RecycleDataViewBehavior, Label):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)


    """ Add selection support to the Label """
    index = None

    def refresh_view_attrs(self, rv, index, data):
        """ Catch and handle the view changes """
        self.index = index
        return super(RVLabel, self).refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(RVLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def on_press(self):
        self.selected = True
        print("Pressed")

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        if is_selected:
            print("I AM SELECTED")
            # opens the page associated with that recipe name
            selection = rv.data[index]["text"]
#            if rv.type == "recipe":
            print("recipe tree")
            self.selected = False
            rv.switch_to_recipe(selection)

            # else:
            #     # Contains type of category and specific category name(e.g. "price":"$$")
            #     rv.update_rec(rv.upper_cat, selection)
            #     print("updating category RV")
        self.selected = False



    def on_release(self, rv, index, is_selected):
        print("on_release: ", rv.data[index])


class RV(RecycleView):
    manager = ObjectProperty(None)
    controller = ObjectProperty(None)
    # determines which RV I am clicking for selectable label
    type = "recipe"
    upper_cat = "home"

    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)

    def switch_to_recipe(self, selection):
        self.controller.switch_recipe(selection)
        self.manager.transition = NoTransition()
        self.manager.last = self.manager.current
        self.manager.current = "recipeView"

    def update_rec(self, high_level_cat, low_level_cat):
        # Set identifier so that SelectableLabel knows what to do on_press
        print("low level cat: ", low_level_cat)
        self.type = "recipe"

        category_dict = {high_level_cat:low_level_cat}
        self.data = [{'text': key} for key in self.controller.get_recipe_list(category_dict)]

    def search_results(self, result_list):
        self.data = [{'text': name} for name in result_list]


class RVScreen(Screen):
    pass


class CategoryLabel(Label):
    pass


class CategoryInput(TextInput):
    pass


class SidebarButton(Button):
    opened = False
    upper_cat = ""
    pass

class HomeScreen(Screen):
    controller = ObjectProperty(None)
    app = ObjectProperty(None)
    rv = ObjectProperty(None)
    catDD = ObjectProperty(None)

    def go_home(self):
        self.ids.Title.text = "All Recipes"
        self.rv.update_rec("","")
        self.manager.current = "home"

    def new_recipe(self):
        self.app.editRecipe.new_recipe()
        self.manager.last = self.manager.current
        self.manager.current = "editRecipe"

    def simple_search(self):
        # print(self.ids.searchbar.text)
        results = self.controller.simple_name_search(self.ids.searchbar.text)
        print(results)
        self.rv.search_results(results)

    # Select function bound to dropdown, low level category buttons
    # input: the instance of the button, which contains upper category and lower category (in text)
    def dropdown_select(self, button):
        self.rv.update_rec(button.upper_cat, button.text.strip())

    # purpose: creates the dropdown menu for an upper level category
    #          when it is selected in the sidebar
    # input: name of upper level category and its index in stack layout
    def create_dropdown(self, upper_cat, index):
        cat_list = self.controller.get_category_list(upper_cat.lower())
        #counts the dropdown buttons created
        btn_count = 0
        # tracks the index at which to add the new buttons in the sidebar
        i = index

        #select = lambda self, current_cat=lower_cat: print(current_cat)
        # Creates buttons for each lower level category associated with the selected
        # upper level category, binds each button to update the recycleview with the selection,
        # and adds the button to the sidebar at the appropriate index
        for lower_cat in cat_list:
            btn = SidebarButton(text="     " + lower_cat)
            btn.upper_cat = upper_cat
            btn.bind(on_release=self.dropdown_select)
            self.ids.sidebarLayout.add_widget(btn, i)
            i -= 1
            btn_count += 1

        # corrects the index attribute in each button that is (visually) below the
        # created sidebar, to make further dropdown creation work
        for button in self.ids.sidebarLayout.children[:i]:
            button.index -= btn_count

    # purpose: removes the dropdown (lower level category) buttons from the sidebar
    # input: the name of the upper level category whose dropdown will be closed, and its index
    #        in the sidebar
    def dismiss_dropdown(self, upper_cat, index):
        cat_list = self.controller.get_category_list(upper_cat.lower())
        btn_count = 0
        for j in range(len(cat_list)):
            self.ids.sidebarLayout.remove_widget(self.ids.sidebarLayout.children[index])
            btn_count += 1

        # corrects the index attribute in each button that is (visually) below the removed sidebar
        for button in self.ids.sidebarLayout.children[:index+1]:
            button.index += btn_count
            #print(button.text, button.index)


class RecipeViewScreen(Screen):
    controller = ObjectProperty(None)
    app = ObjectProperty(None)
    recipe_info = {}

    # Sets the screen's text to show the input recipe's info
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

    # Switch to editing the recipe that is currently being viewed
    def edit_recipe(self):
        # Fill the edit screen with the current recipe's info
        self.app.editRecipe.fill_recipe(self.recipe_info)

        # Then go to that screen
        self.manager.last = self.manager.current
        self.manager.current = "editRecipe"

class EditRecipeScreen(Screen):
    controller = ObjectProperty(None)
    app = ObjectProperty(None)
    # Unique identifier to show the recipe being edited is new
    NEW_ID = "#*$&^#*($&#"
    # The recipe ID will be set to the recipe name once it is saved
    recipe_id = NEW_ID

    # Sets the screen's text to show the input recipe's info
    def fill_recipe(self, recipe_info):
        if recipe_info == None:
            print("Invalid recipe")
            self.manager.last = self.manager.current
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

    # Set the screen's text to be an empty recipe
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

    # Save the entered text, controller decides whether it is a new or existing recipe
    def save_recipe(self):
        new_info = {
            "name": self.ids.name.text,
            "ingredients": self.ids.ingredients.text,
            "instructions": self.ids.instructions.text,
            "category": self.ids.category.text[10:],
            "meal": self.ids.meal.text[6:],
            "prep time": self.ids.prep.text[11:],
            "difficulty": self.ids.difficulty.text[12:],
            "price": self.ids.price.text[7:],
            "ethnicity": self.ids.ethnicity.text[11:]}

        self.controller.save_recipe(self.recipe_id, new_info)

        #update the recipe screen with the new recipe information
        self.app.home.rv.update_rec("","")
        #switch to the recipe screen
        self.controller.switch_recipe(new_info["name"])
        self.manager.transition = NoTransition()
        self.manager.last = self.manager.current
        self.manager.current = "recipeView"

    # Delete the recipe currently being edited
    def delete_recipe(self):
        # If it is a new recipe, no entry was ever made in database
        if self.recipe_id == self.NEW_ID:
            self.manager.last = self.manager.current
            self.manager.current = "home"
        # If the user was editing an existing recipe, it must be deleted from database
        else:
            self.controller.delete_recipe(self.recipe_id)
            self.app.home.rv.update_rec()
            self.manager.last = self.manager.current
            self.manager.current = "home"


class KivyViewApp(App):
    manager = ObjectProperty(None)
    home = ObjectProperty(None)
    recipeView = ObjectProperty(None)
    editRecipe = ObjectProperty(None)
    controller = ObjectProperty(None)

    def build(self):
        self.manager = self.instantiate()
        return self.manager

    # Create and fill the screen manager at the app level
    def instantiate(self):
        screen_man = ScreenManager()
        self.home = HomeScreen(name="home", controller=self.controller, app=self)
        self.recipeView = RecipeViewScreen(name="recipeView", controller=self.controller, app=self)
        self.editRecipe = EditRecipeScreen(name="editRecipe", controller=self.controller, app=self)
        screen_man.add_widget(self.home)
        screen_man.add_widget(self.recipeView)
        screen_man.add_widget(self.editRecipe)
        # create a variable to implement < and > buttons
        screen_man.last = "home"
        return screen_man

    # returns initial list of recipe names for recycleview instantiation
    def gen_rv_recs(self):
        home_dict = {"":""}
        return [{'text': key} for key in self.controller.get_recipe_list(home_dict)]

    def simple_search(self, search_text):
        search_results = self.controller.simple_name_search(search_text)
        self.home.rv.update_rec(search_results)


class View:
    def __init__(self, controller_in):
        self.app = KivyViewApp()
        self.app.controller = controller_in

    # Separate run from init to allow view instantiation in controller, before running pauses everything
    def run_app(self):
        self.app.run()
