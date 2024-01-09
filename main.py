from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle
from kivy.core.window import Window

class Gamewidget(Widget):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        with self.canvas :
            self.door = Rectangle(source='door.png',pos=(600,0),size=(200,200))
            self.player = Rectangle(source='player.png',pos=(0,50),size=(200,400))

class SleepWell(App):
    def build(self):
        return Gamewidget()
    
if __name__ == '__main__' :
    app = SleepWell()
    app.run()