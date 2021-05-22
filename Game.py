from Point import Point

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

DIR = os.path.dirname(__file__) + '/../'
KEY_REPEAT_DELAY = 200
KEY_REPEAT_INTERVAL = 20
FPS = 30
START_FULLSCREEN = False

class Game:
    def __init__(self, size = [None, None], title = 'Hello World!', args=None):

        self.args = args
        self.backgroundColor = [30, 30, 30]
        self.fps = FPS

        #* Initialize Pygame
        pygame.init()
        self.clock = pygame.time.Clock()
        pygame.mouse.set_visible(True)
        tmp = pygame.display.Info(); self.screenSize = (tmp.current_w, tmp.current_h)
        pygame.key.set_repeat(KEY_REPEAT_DELAY, KEY_REPEAT_INTERVAL)
        pygame.display.set_caption(title)

        self.fullscreenWindowFlags = pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.FULLSCREEN | pygame.NOFRAME
        self.windowedWindowFlags   = pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.RESIZABLE

        if pygame.__version__ >= '2.0.0':
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)
            pygame.display.set_allow_screensaver(True)
            self.windowedWindowFlags = self.windowedWindowFlags | pygame.SCALED

        #* Set the icon
        # with open(DIR + 'data/' + self.settings['iconFile'], 'r') as icon:
        #     pygame.display.set_icon(pygame.image.load(icon))

        self.windowedSize = size
        if size[0] is None:
            self.windowedSize[0] = round(self.screenSize[0] / 1.5)
        if size[1] is None:
            self.windowedSize[1] = round(self.screenSize[1] / 1.5)

        if START_FULLSCREEN:
            self.mainSurface = pygame.display.set_mode(self.screenSize, self.fullscreenWindowFlags)
        else:
            self.mainSurface = pygame.display.set_mode(self.windowedSize, self.windowedWindowFlags)
        
        #* Get info about the graphics
        vidInfo = pygame.display.Info()
        if self.args.verbose:
            print('Backend video driver being used:', pygame.display.get_driver())
            print('The display is', 'not' if not vidInfo.hw else '', 'hardware accelerated')
            print('The display has', vidInfo.video_mem, 'MB of video memory')
            print('The current width and height of the window are:', (vidInfo.current_w, vidInfo.current_h))
            print('The width and height of the display is:', self.screenSize)


    def getSize(self):
        #* This won't work until pygame 2.0.0
        # return pygame.display.get_window_size()
        tmp = pygame.display.Info()
        return [tmp.current_w, tmp.current_h]


    def updateMouse(self):
        self.mouseLoc = Point(*pygame.mouse.get_pos())


    def run(self):
        run = True
        fullscreen = False

        while run:
            deltaTime = self.clock.tick(self.fps) / 1000.0
            
            for event in pygame.event.get():
                #* Exit the window
                if event.type == pygame.QUIT:
                    self.exit()

                #* Mouse moves
                if event.type == pygame.MOUSEMOTION:
                    self.updateMouse()

                #* If the left mouse button is released
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    pass
                    
                #* Right mouse button clicked or c is pressed
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                    pass

                #* If a file is dropped into the window
                if event.type == pygame.DROPFILE and event.file[-4:0] == '.gdl':
                    pass

                #* If you scroll up
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
                    pass

                #* If you scroll down
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
                    pass

                #? Keys here
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.exit()
                    if event.key == pygame.K_UP    or event.unicode == 'w':
                        pass
                    if event.key == pygame.K_DOWN  or event.unicode == 's':
                        pass
                    if event.key == pygame.K_LEFT  or event.unicode == 'a':
                        pass
                    if event.key == pygame.K_RIGHT or event.unicode == 'd':
                        pass
                    if event.unicode == 'f':
                        # pygame.display.toggle_fullscreen()
                        if not fullscreen:
                            self.mainSurface = pygame.display.set_mode(self.screenSize, self.fullscreenWindowFlags)
                        else:
                            self.mainSurface = pygame.display.set_mode(self.windowedSize, self.windowedWindowFlags)

                        fullscreen = not fullscreen
                    if event.unicode in ['S', '\x13']: #* ctrl + s
                        pass
                    
            #* Draw stuff here
            self.draw()

            pygame.display.flip()
            pygame.display.update()
            self.mainSurface.fill(self.backgroundColor)


    def draw(self):
        pass


    def exit(self):
        pygame.quit()
        quit()


""" 
    def drawLines(self):
        for line in self.lines:
            line.draw(self.mainSurface)
        for line in self.metaLines:
            line.draw(self.mainSurface)
"""
""" 
    def drawDots(self):
        for i in self.dots:
            pygame.draw.rect(self.mainSurface, self.settings['dotColor'], pygame.Rect(i.data(), [self.settings['dotSize'], self.settings['dotSize']]))
"""
""" 
    def getLinesWithinRect(self, bounds):
        ''' bounds is a pygame.Rect '''

        patternLines = []
        halfLines = []
        patternLineIndecies = []
        halfLineIndecies = []

        #* Because the collidePoint function returns True if a line is touching 
        #*  the left or top, but not the bottom or right, we have to inflate the
        #*  rectangle and then move it so it's positioned correctly
        incBounds = bounds.inflate(self.settings['dotSpread'], self.settings['dotSpread'])
        incBounds.move_ip(self.settings['dotSpread'] / 2, self.settings['dotSpread'] / 2)

        #* Get all the lines that are in the incBounds, and the halfway in lines seperately
        for index, l in enumerate(self.lines):
            if incBounds.collidepoint(l.start.data()) and incBounds.collidepoint(l.end.data()):
                patternLines.append(l)
                patternLineIndecies.append(index)
            elif incBounds.collidepoint(l.start.data()) or incBounds.collidepoint(l.end.data()):
                halfLines.append(l)
                halfLineIndecies.append(index)

        return [patternLines, halfLines, patternLineIndecies, halfLineIndecies]
"""


'''
    def text_objects(self, text, font):
        textSurface = font.render(text, True, namedColor('black').color)
        return textSurface, textSurface.get_rect()

    def message_display(self, text):
        largeText = pygame.font.Font('freesansbold.ttf', 115)
        TextSurf, TextRect = self.text_objects(text, largeText)
        TextRect.center = ((display_width / 2),(display_height / 2))
        self.mainSurface.blit(TextSurf, TextRect)

        pygame.display.update()
        # time.sleep(2)
        self.run()
'''


import argparse
description = ''
parser = argparse.ArgumentParser(description=description)
parser.add_argument('-v' , '--verbose' , action='store_true')
args = parser.parse_args()

game = Game(title='GeoDoodle', args=args)
game.run()
game.exit()