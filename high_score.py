import pygame
from pygame.locals import *

class High_Score(object):
    def __init__(self, window):
        """
        Game constructor.
        """
        self.window = window

        self.background = pygame.Surface( self.window.get_size() )
        self.background = self.background.convert()
        self.background.fill( (0, 0, 0) )

        if pygame.font:
            font_menu = pygame.font.Font('fonts/casio-fx-702p.ttf', 70)#
            self.text_menu = font_menu.render( "high scores", 1, (200, 200, 200), (0, 0, 0) )
            self.text_menu_pos = self.text_menu.get_rect( centerx = self.window.get_width()/2, \
                                                            centery = self.window.get_height() * 3/20 )
    
        self.clock = pygame.time.Clock()

    def run(self):
        """
        Game loop
        """

        while not self.handle_events():
            self.clock.tick(60)
            
            self.background.blit( self.text_menu, self.text_menu_pos )
            self.window.blit( self.background, (0, 0))

            pygame.display.flip()
            

    def handle_events(self):
            """
            Handling system events

            :return True if pygame reported a quit event
            """
            for event in pygame.event.get():
                if event.type == pygame.locals.QUIT:
                    pygame.quit()
                    sys.exit()
                    return True
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    return True
