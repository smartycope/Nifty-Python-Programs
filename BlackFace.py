#!/bin/python

# Pygame version
'''
import pygame

FPS = 1
START_FULLSCREEN = True
from os.path import dirname, join; DIR = join(dirname(__file__), '..')


class Game:
    def __init__(self, size = [None, None], title = 'Hello World!', args=None):

        self.args = args
        self.fps = FPS

        self.initPygame(size, title)


    def run(self):
        while True:
            deltaTime = self.clock.tick(self.fps) / 1000.0

            for event in pygame.event.get():
                pygame.event.pump()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit(0)

            pygame.display.update()

            self.mainSurface.set_alpha(100)

            self.mainSurface.fill([0, 0, 0, 140])


    def initPygame(self, size, title):
        #* Initialize Pygame
        pygame.init()
        self.clock = pygame.time.Clock()
        pygame.mouse.set_visible(True)
        tmp = pygame.display.Info()
        self.screenSize = (tmp.current_w, tmp.current_h)

        pygame.display.set_caption(title)

        self.fullscreenWindowFlags = pygame.NOFRAME | pygame.RESIZABLE

        if pygame.__version__ >= '2.0.0':
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)
            pygame.display.set_allow_screensaver(True)

        #* Set the icon
        # with open(DIR + 'data/' + self.settings['iconFile'], 'r') as icon:
        #     pygame.display.set_icon(pygame.image.load(icon))

        self.mainSurface = pygame.display.set_mode(self.screenSize, self.fullscreenWindowFlags)
        # pygame.display.toggle_fullscreen()


game = Game()
game.run()
'''

# wxPython version
'''
import wx

class Window(wx.App):
    def OnInit(self):
        # frame = wx.Frame(parent=None, title='Bare')
        # frame.Show()
        window = wx.Window(parent=None, style=wx.TRANSPARENT_WINDOW)

        if not window.SetTransparent(100):
            print("This system does not support transparent windows, sorry.")

        window.Show()
        return True


app = Window()
app.MainLoop()
'''

# tkinter version
from tkinter import Tk

transparency = .7
root = Tk()
keyChangeAmount = 0.05

def keyHandler(event):
    global transparency, root

    # print(event.char, event.keysym, event.keycode, event.delta, event.num, sep='\t')

    if event.keycode == 9: # Escape
        exit(0)

    if event.keysym == 'Up':
        transparency += keyChangeAmount
        root.wm_attributes('-alpha', transparency)

    if event.keysym == 'Down':
        transparency -= keyChangeAmount
        root.wm_attributes('-alpha', transparency)

    if event.num == 4 or event.delta > 0: # Scrolling down
        transparency -= keyChangeAmount
        root.wm_attributes('-alpha', transparency)

    if event.num == 5 or event.delta < 0: # Scrolling up
        transparency += keyChangeAmount
        root.wm_attributes('-alpha', transparency)


root.bind("<Escape>", keyHandler)
root.bind("<MouseWheel>", keyHandler)
root.bind("<Button-4>", keyHandler)
root.bind("<Button-5>", keyHandler)
root.bind("<Up>", keyHandler)
root.bind("<Down>", keyHandler)

root.wait_visibility(root)
root.wm_attributes('-alpha', transparency)
root.configure(background='black')
root.wm_attributes('-fullscreen', 'true')

root.mainloop()
