from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.popup import Popup

Builder.load_string('''
#:kivy 1.10.0
#: import Popup kivy.uix.popup

<MessageBox>:
    title: 'Popup Message Box'
    size_hint: None, None
    size: 400, 400

    BoxLayout:
        orientation: 'vertical'
        Label:
            text: root.message
        Button:
            size_hint: 1, 0.2
            text: 'OK'
            on_press: root.dismiss()

<RecycleViewRow>:
    orientation: 'horizontal'
    Button:
        text: root.text
        on_press: app.root.message_box(root.text)

<MainScreen>:
    viewclass: 'RecycleViewRow'
    RecycleBoxLayout:
        default_size: None, dp(56)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        orientation: 'vertical'                    
                    ''')

from model_w_recipe import *
model = RecipeBook("andrew", "password", "localhost", "recipes", "recipes", "ingredients", "recipe_name")


class MessageBox(Popup):
    message = StringProperty()


class RecycleViewRow(BoxLayout):
    text = StringProperty()


class MainScreen(RecycleView):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        rec_list = self.build_recipe_list("", "")
        self.data = [{'text': recipe, 'id': recipe} for recipe in rec_list]

    def build_recipe_list(self, category, value):
        search_dictionary = {value: category}
        return model.filter_recipes(search_dictionary)


    def message_box(self, message):
        p = MessageBox()
        p.message = message
        p.open()
        print('test press: ', message)

class TestApp(App):
    title = "RecycleView Direct Test"

    def build(self):
        return MainScreen()


TestApp().run()