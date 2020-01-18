from kivy.app import App
# from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen

# RecycleView stuff
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import BooleanProperty
from kivy.properties import NumericProperty
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.label import Label
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import ListProperty, StringProperty, ObjectProperty
from kivy.uix.dropdown import DropDown
from kivy.uix.textinput import TextInput


from recipes_controller import *
controller = Controller()

s_m = ScreenManager()

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


#    def on_press(self):
#        self.selected = True


    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        if is_selected:
	        controller.open_recipe_page(rv.data[index])
            #print("selection changed to {0}".format(rv.data[index]))
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


class ScreenManagerApp(App):

    def build(self):
        root = ScreenManager()
        root.add_widget(CustomScreen(name='CustomScreen'))
        root.add_widget(RVScreen(name='RVScreen'))
        return root

class CustomDropDown(DropDown):
    pass



class HomeScreen(Screen):
	recipe_list = ObjectProperty()

	def tester(self):
		print("Test complete")

	def fill_recipe_page(self, recipe_name):
		info_dict = controller.open_recipe_page(recipe_name)
		for item in info_dict:
			print(item)
		root.manager.current
		return


class RecipeViewScreen(Screen):
	pass


class MyScreenManager(ScreenManager):
	pass


class testApp(App):
	def build(self):
		screen_manager = MyScreenManager()
		s_m = screen_manager
		return screen_manager
		#return RecipeViewScreen()
		#return HomeScreen()


print("POOP")
testApp().run()
