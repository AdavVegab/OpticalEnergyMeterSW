from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, NoTransition
from kivy.uix.gridlayout import GridLayout


x = []


class MainScreen(GridLayout):
     pass



class OEMApp(App):
    def build(self):
          return MainScreen()

if __name__ == '__main__':
    OEMApp().run()