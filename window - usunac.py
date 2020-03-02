import pygame
import os

class Window(object):
    """
    Window of game. Responsible for drawing the game window.
    """

    def __init__(self):
        """
        Game window constructor. Prepares the game window.
        """

        infoObject = pygame.display.Info() # Gets information about the screen
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % ( 0, 0 ) # The initial position of the window on the screen
        self.surface = pygame.display.set_mode(( infoObject.current_w, infoObject.current_h)) # Creating a game window
        pygame.display.set_caption("Pong game") # Name of the game window

        self.background = pygame.Surface( self.surface.get_size() )
        self.background = self.background.convert()

    def draw(self, *args):
        """
        Draws game window

        :param args: list of elements to draw
        """

        self.background.fill( (0, 0, 0) )

        for drawable in args:
            self.background.blit( drawable[0], drawable[1] )
        
        self.surface.blit( self.background, (0, 0))
        pygame.display.update()

    def get_width( self ):
        """
        Returns width of game window
        """

        return self.surface.get_width()

    def get_height( self ):
        """
        Returns height of game window
        """

        return self.surface.get_height()
