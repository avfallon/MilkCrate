from kivy.app import App
from kivy.properties import BooleanProperty, ObjectProperty
from kivy.properties import NumericProperty
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

        else:
            print("selection removed for {0}".format(rv.data[index]))

    def on_release(self, rv, index, is_selected):
        print(rv.data[index])


class RV(RecycleView):
    manager = ObjectProperty(None)
    controller = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)

    def update(self):
        print("Updating recipe list")
        self.data = [{'text': key} for key in self.controller.get_recipe_list()]

class RVScreen(Screen):
    pass

class CategoryLabel(Label):
    pass

class HomeScreen(Screen):
    controller = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)

    def view_recipe(self):
        self.manager.current = "recipeView"


class RecipeViewScreen(Screen):
    controller = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(RecipeViewScreen, self).__init__(**kwargs)

    def update_recipe(self, recipe_info):
        self.ids.ingredients.text = recipe_info["ingredients"]
        self.ids.instructions.text = recipe_info["instructions"]
        self.ids.category.text = self.ids.category.text + recipe_info["category"]
        self.ids.meal.text = self.ids.meal.text + recipe_info["meal"]
        self.ids.ethnicity.text = self.ids.ethnicity.text + recipe_info["ethnicity"]
        self.ids.difficulty.text = self.ids.difficulty.text + recipe_info["difficulty"]
        self.ids.price.text = self.ids.price.text + recipe_info["price"]
        self.ids.prep.text = self.ids.prep.text + recipe_info["prep time"]


    def go_home(self):
        self.manager.current = "home"


class TestApp(App):
    manager = ObjectProperty(None)
    home = ObjectProperty(None)
    recipeView = ObjectProperty(None)
    controller = ObjectProperty(None)

    def build(self):
        self.manager = self.instantiate()
        return self.manager

    def instantiate(self):
        screen_man = ScreenManager()
        self.home = HomeScreen(name="home", controller=self.controller)
        self.recipeView = (RecipeViewScreen(name="recipeView", controller=self.controller))
        screen_man.add_widget(self.home)
        screen_man.add_widget(self.recipeView)
        return screen_man

    # returns list of recipe names for recycleview instantiation
    def gen_rv_data(self):
        return [{'text': key} for key in self.controller.get_recipe_list()]


class View:
    def __init__(self, controller_in):
        self.app = TestApp()
        self.app.controller = controller_in
        self.test = "hellooo"

    def run_app(self):
        self.app.run()
