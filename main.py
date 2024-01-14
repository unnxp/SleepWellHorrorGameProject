from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.uix.label import Label
from kivy.animation import Animation
from kivy.uix.image import Image 

class ClockDisplay :
    def __init__(self,hourv,minutev):
        self.hour = NumberDisplay(hourv)
        self.minute = NumberDisplay(minutev)
        
    
    def tick(self):
        self.minute.tick()
        if self.minute.v == 60:
            self.minute.v = 0
            self.hour.tick()
    
    def display(self):
        return '{:02d}:{:02d}'.format(self.hour.v,self.minute.v)

class NumberDisplay:
    def __init__(self,initv) :
        self.v = initv
    def tick(self):
        self.v = self.v + 1        

class Gamewidget(Widget):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._on_keyboard_closed,self)
        self._keyboard.bind(on_key_down=self._on_key_down)
        self._keyboard.bind(on_key_up=self._on_key_up)
        self.clock_display = ClockDisplay(0, 0)
        self.register_event_type('on_frame')
        

        with self.canvas :
            Rectangle(source='BackGR1.png',pos=(0,0),size=(Window.width,Window.height))
            self.clock_label = Label(text='', font_size=20, pos=(20, Window.height - 100))
        
        self.soundBack = SoundLoader.load('backgroundsound1.wav')
        if self.soundBack:
            # Set the sound to loop
            self.soundBack.loop = True
                # Play the sound
            self.soundBack.play()
        
        self.keysPressed = set()
        self._entities = set()

        Clock.schedule_interval(self._on_frame,0.375)
        Clock.schedule_interval(self.update_clock_label, 1)

        
    def _on_frame(self,dt):
        self.dispatch('on_frame',dt)

    def on_frame(self,dt):
        pass

        
    def add_entity(self,entity):
        self._entities.add(entity)
        self.canvas.add(entity._instruction)

    def remove_entity(self,entity):
        if entity in self._entities:
            self._entities.remove(entity)
            self.canvas.remove(entity._instruction)
    def collides(self,e1,e2):
        r1x = e1.pos[0]
        r1y = e1.pos[1]
        r2x = e2.pos[0]
        r2y = e2.pos[1]
        r1w = e1.size[0]
        r1h = e1.size[1]
        r2w = e2.size[0]
        r2h = e2.size[1]

        if(r1x < r2x + r2w and r1x + r1w > r2x and r1y < r2y + r2h and r1y + r1h > r2y):
            return True
        else :
            return False
        
    def colliding_entities(self,entity):
        result = set()
        for e in self._entities :
            if self.collides(e,entity) and e == entity :
                result.add(e)
        return result

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
    
    def update_clock_label(self, dt):
        self.clock_display.tick()
        self.clock_label.text = f"Time: {self.clock_display.display()}"

class Entity(object):
    def __init__(self):
        self._pos = (0,0)
        self._size = (50,50)
        self._source = 'example.png'
        self._instruction = Rectangle(pos=self._pos,size=self._size,source=self._source)
    @property
    def pos(self):
        return self._pos
    
    @pos.setter
    def pos(self,value):
        self._pos = value
        self._instruction.pos = self._pos
    
    @property
    def size(self):
        return self._size
    
    @size.setter
    def size(self,value):
        self._size = value
        self._instruction.size = self._size

    @property
    def source(self):
        return self._source
    
    @source.setter
    def source(self,value):
        self._source = value
        self._instruction.source = self._source

class Door(Entity):
    def __init__(self):
        super().__init__()
        self.source = 'door.png'
        self.size = (110,250)
        self.pos = (340,160)
    def on_frame(self, dt=None):
        pass

class Candle(Entity):
    def __init__(self):
        super().__init__()
        self.source = 'candle1.png'
        self.size = (100,120)
        self.pos = (100,250)
        self.lst_source = ['candle1.png', 'candle2.png', 'candle3.png', 'candle4.png', 'candle5.png', 'candle6.png', 'candle7.png']
        self.animation_interval = 0.08
        self.animate_candle()
    def on_frame(self, dt=None):
        pass   

    def animate_candle(self, dt=None):
        current_index = self.lst_source.index(self.source)
        next_index = (current_index + 1) % len(self.lst_source)
        self.source = self.lst_source[next_index]
        Clock.schedule_once(self.animate_candle, self.animation_interval)

class Phone(Entity) :    
    def __init__(self):
        super().__init__()
        self.source = 'phone1.png'
        self.size = (200,180)
        self.pos = (600,50)
    def on_frame(self,dt=None):
        pass

class Player(Entity):
    def __init__(self):
        super().__init__()
        
        self.source = 'player.png'
        self.size = (150, 300)
        self.pos = (0, 0)
        self.moving_right = False
        self.moving_left = False
        self.load_walk_images()
        game.bind(on_frame=self.on_frame)

        self.soundwalk1 = SoundLoader.load('stepfoot1.wav')     
        self.soundwalk2 = SoundLoader.load('stepfoot2.wav')
        self.soundwalk3 = SoundLoader.load('stepfoot3.wav')

    def load_walk_images(self):
        self.walk_images_right = ['RW1.png', 'RW2.png']
        self.walk_images_left = ['LW1.png', 'LW2.png']
        self.walk_index = 0

    def stop_callback(self):
        game.unbind(on_frame=self.on_frame)

    def on_frame(self, sender, dt):
        step_size = 200 * dt
        newx = self.pos[0]
        newy = self.pos[1]

        if 'a' in game.keysPressed:
            newx -= step_size
            self.moving_left = True
            self.moving_right = False
        elif 'd' in game.keysPressed:
            newx += step_size
            self.moving_right = True
            self.moving_left = False
        else:
            self.moving_left = False
            self.moving_right = False
        newx = max(0, min(newx, Window.width - self.size[0]))
        newy = max(0, min(newy, Window.height - self.size[1]))

        self.pos = (newx, newy)

        if 'e' in game.keysPressed:
            # This is where you can handle the action when 'e' is pressed
            pass

        self.update_walk_animation()

    def update_walk_animation(self):
        if self.moving_right:
            self.source = self.walk_images_right[self.walk_index]
            self.play_footstep_sound()
        elif self.moving_left:
            self.source = self.walk_images_left[self.walk_index]
            self.play_footstep_sound()

        self.walk_index = (self.walk_index + 1) % len(self.walk_images_right)
    
    def play_footstep_sound(self):
        if self.walk_index == 0:
            self.soundwalk1.play()
        elif self.walk_index == 1:
            self.soundwalk2.play()

game = Gamewidget()
game.door = Door()
game.add_entity(game.door)
game.phone = Phone()
game.add_entity(game.phone)
game.candle = Candle()
game.add_entity(game.candle)
game.player = Player()
game.add_entity(game.player)


class SleepWell(App):
    def build(self):
        
        return game

if __name__ == '__main__' :
    app = SleepWell()
    app.run()