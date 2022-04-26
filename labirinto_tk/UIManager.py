import tkinter as tk
import mp3play


class Window:
    def __init__(self):
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        self.tk = tk.Tk()
        self.tk.geometry(str(self.SCREEN_WIDTH)+'x'+str(self.SCREEN_HEIGHT))
        self.tk.resizable(False, False)
        self.tk.config(cursor="none")
        self.canv = None
        self.game_is_on = False

    def set_fullscreen(self):
        self.tk.attributes('-fullscreen', True)
        self.SCREEN_WIDTH = self.tk.winfo_screenwidth()
        self.SCREEN_HEIGHT = self.tk.winfo_screenheight()

    def set_screen_resolution(self, x, y):
        self.SCREEN_WIDTH = x
        self.SCREEN_HEIGHT = y
        self.tk.geometry(str(self.SCREEN_WIDTH)+'x'+str(self.SCREEN_HEIGHT))

    def start_menu(self):
        pass

    def show_canvas(self):
        self.canv = tk.Canvas(self.tk, bg='white')
        self.canv.pack(fill=tk.BOTH, expand=1)
        self.tk.config(cursor="none")
        self.game_is_on = True

    def pause(self):
        self.canv.destroy()
        self.game_is_on = False

    @staticmethod
    def close():
        quit()


class SoundManager:
    def __init__(self):
        self.sounds = {}

    def add(self, name, path):
        self.sounds[name] = {'id': mp3play.load(path), 'path': path}

    def play(self, name, **kwargs):
        self.sounds[name]['state'] = 'on'
        self.sounds[name]['id'].play(**kwargs)

    def stop(self, name, **kwargs):
        self.sounds[name]['state'] = 'off'
        self.sounds[name]['id'].stop(**kwargs)

    def isPlaying(self, name):
        return self.sounds[name]['id'].isplaying()


class ImageManager:
    def __init__(self):
        self.images = {}

    def add(self, name, path):
        self.images[name] = {'id': tk.PhotoImage(file=path), 'path': path}
        self.images[name]['id'].image = self.images[name]['id']

    def draw(self, name, x=0, y=0):
        self.images[name]['img'] = tk.Label(image=self.images[name]['id'])
        self.images[name]['img'].place(x=x, y=y)

    def undraw(self, name):
        self.images[name]['img'].destroy()

    def place(self, name, x, y):
        self.images[name]['img'].place(x=x, y=y)


class Button:
    def __init__(self, window, text='', x=0, y=0):
        self.id = tk.Button(window.tk, text=text)
        self.text = text
        self.place = (x, y)
        self.id.place(x=x, y=y)

    def set_place(self, x, y):
        self.id.place(x=x, y=y)
        self.place = (x, y)

    def bind(self, command, function):
        self.id.bind(command, function)


class Label:
    def __init__(self, text='', width=20, height=2, bg='grey', font='30', x=0, y=0):
        self.text = text
        self.place = (x, y)
        self.width = width
        self.height = height
        self.bg = bg
        self.font = font
        self.id = tk.Label(width=width, height=height, bg=bg, text=text, font=font)
        self.id.place(x=x, y=y)

    def set_place(self, x, y):
        self.id.place(x=x, y=y)
        self.place = (x, y)


class BindingManager:
    def __init__(self, window):
        self.bindings = {}
        self.window = window
        self.pressed = set()
        window.tk.bind('<KeyPress>', self._keyPressed)
        window.tk.bind('<KeyRelease>', self._keyReleased)

    def bind(self, name, *keys):
        self.bindings[name] = {*keys}

    def add_keys(self, name, *keys):
        self.bindings[name].update([*keys])

    def del_keys(self, name, *keys):
        self.bindings[name].discard([*keys])

    def isPressed(self, name):
        for key in self.bindings[name]:
            if key not in self.pressed:
                return False
        return True

    def _keyPressed(self, event):
        self.pressed.add(event.keycode)
        pass

    def _keyReleased(self, event):
        self.pressed.discard(event.keycode)
        pass
