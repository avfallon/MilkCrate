from kivy.app import App
from kivy.properties import BooleanProperty
from kivy.properties import NumericProperty
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.label import Label
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.dropdown import DropDown
from kivy.uix.textinput import TextInput


from recipes_controller import *
controller = Controller()


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
            print("yaya")
            name = rv.data[index]["text"]
            print(name)
            recipe_info = controller.get_recipe_info(name)
            print(recipe_info)


        else:
            print("selection removed for {0}".format(rv.data[index]))


    def on_release(self, rv, index, is_selected):
        print(rv.data[index])


class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.data = controller.make_recipe_list()


class RVScreen(Screen):
    pass


class CustomDropDown(DropDown):
    pass


class HomeScreen(Screen):
    recipe_list = ObjectProperty()

    # opens and fills recipe page with information from database
    def fill_recipe_page(self, recipe_name):
        info_dict = controller.open_recipe_page(recipe_name)
        print("Fill_recipe_page")
        self.manager.current = "recipeView"
        return


class RecipeViewScreen(Screen):
    pass


class TestApp(App):

    def build(self):
        screen_man = ScreenManager()

        home = HomeScreen(name="home")
        test_rv = RV()

        recipe_view = RecipeViewScreen(name="recipeView")

        screen_man.add_widget(home)
        screen_man.add_widget(recipe_view)
        return screen_man

    def instantiate(self):
        screen_man = ScreenManager()

        home = HomeScreen(name="home")
        test_rv = RV()

        recipe_view = RecipeViewScreen(name="recipeView")

        screen_man.add_widget(home)
        screen_man.add_widget(recipe_view)
        return screen_man

    # returns app.run
    def recipe_click(self):
        print("hello")



print("POOP")
#TestApp().run()
