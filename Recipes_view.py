from kivy.app import App
from kivy.uix.label import Label


class SimpleKivy(App):
	def build(self):
		return Label(text="Ingredients")

SimpleKivy().run()
