from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.core.audio import SoundLoader

def collides(rect1,rect2):
    r1x = rect1[0][0]
    r1y = rect1[0][1]
    r2x = rect2[0][0]
    r2y = rect2[0][1]
    r1w = rect1[1][0]
    r1h = rect1[1][1]
    r2w = rect2[1][0]
    r2h = rect2[1][1]

    if(r1x < r2x + r2w and r1x + r1w > r2x and r1y < r2y + r2h and r1y + r1h > r2y):
        return True
    else :
        return False



class Gamewidget(Widget):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._on_keyboard_closed,self)
        self._keyboard.bind(on_key_down=self._on_key_down)
        self._keyboard.bind(on_key_up=self._on_key_up)

        with self.canvas :
            self.player = Rectangle(source='player.png',pos=(0,50),size=(200,400))

            self.soundwalk1 = SoundLoader.load('stepfoot1.wav')     
            self.soundwalk2 = SoundLoader.load('stepfoot2.wav')
            self.soundwalk3 = SoundLoader.load('stepfoot3.wav')
            self.soundwalk4 = SoundLoader.load('stepfoot2.wav')
            self.soundBack = SoundLoader.load('backgroundsound1.wav')
            if self.soundBack:
                # Set the sound to loop
                self.soundBack.loop = True
                # Play the sound
                self.soundBack.play()
        
        self.keysPressed = set()
        self.animation_counter_d = 0
        self.animation_counter_a = 0
        Clock.schedule_interval(self.move_step,0.45)
        Clock.schedule_interval(self.animate_player_d, 0.45)
        Clock.schedule_interval(self.animate_player_a, 0.45)


    def _on_keyboard_closed(self):
        self._key_board.unbind(on_key_down=self.on_key_down)
        self._keyboard = None
    
    def _on_key_down(self,keyboard,keycode,text,modifiers):
        self.keysPressed.add(text)

    def _on_key_up(self,keyboard,keycode):
        text = keycode[1]
        if text in self.keysPressed:
            self.keysPressed.remove(text)
            self.player.source = 'player.png'
            self.animation_counter = 0

    def move_step(self,dt):
        currentx = self.player.pos[0]
        currenty = self.player.pos[1]
        step_size = 100*dt
        if 'a' in self.keysPressed :
            currentx -= step_size
            self.animation_counter_a += 1

        if 'd' in self.keysPressed :
            currentx += step_size   
            self.animation_counter_d += 1

        self.player.pos = (currentx,currenty)
        #if collides((self.player.pos,self.player.size),(self.door.pos,self.door.size)):
            #print('colliding!')
        #else :
            #print('not colliding')
    
    def animate_player_d(self, dt):
        if 'd' in self.keysPressed:
            if self.animation_counter_d % 2 == 0:
                self.player.source = 'RW1.png'
                self.soundwalk1.play()
            else:
                self.player.source = 'RW2.png'
                self.soundwalk2.play()
    def animate_player_a(self, dt):
        if 'a' in self.keysPressed:
            if self.animation_counter_a % 2 == 0:
                self.player.source = 'LW1.png'
                self.soundwalk3.play()
            else:
                self.player.source = 'LW2.png'
                self.soundwalk4.play()

    def animate_player(self, dt):
        # Handle animation based on direction (left or right)
        if 'a' in self.keysPressed:
            self.animate_left()
        elif 'd' in self.keysPressed:
            self.animate_right()
class SleepWell(App):
    def build(self):
        return Gamewidget()

if __name__ == '__main__' :
    app = SleepWell()
    app.run()