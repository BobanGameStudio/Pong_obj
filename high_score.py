import pygame
from pygame.locals import *
from load import make_text

class High_Score(object):
    def __init__(self, window):
        """
        High Score constructor.
        """
        self.window = window

        self.background = pygame.Surface( self.window.get_size() )
        self.background = self.background.convert()
        self.background.fill( (0, 0, 0) )

        self.window.blit( self.background, (0, 0))

        self.text_highscores, self.text_highscores_pos = make_text( text= "High scores", font_name= 'casio-fx-702p\casio-fx-702p.ttf'\
                                                            , size= 70, pos= (self.window.get_width()/2, self.window.get_height() * 3/20)\
                                                            , text_color= (200, 200, 200), text_background_color= (0, 0, 0))
        self.text_highscores_des, self.text_highscores_des_pos = make_text( text= "(only from pve)", font_name= 'casio-fx-702p\casio-fx-702p.ttf'\
                                                            , size= 25, pos= (self.window.get_width()/2, self.window.get_height() * 4/20)\
                                                            , text_color= (200, 200, 200), text_background_color= (0, 0, 0))

        self.window.blit( self.text_highscores, self.text_highscores_pos )
        self.window.blit( self.text_highscores_des, self.text_highscores_des_pos ) 
        
        with open( "highscores/High Scores.txt" ) as file:
            for i, wiersz in enumerate( file ):
                self.points, self.points_pos = make_text( text= "%.f" %int(wiersz), font_name= 'casio-fx-702p\casio-fx-702p.ttf'\
                                                            , size= 30, pos= (self.window.get_width()* 1/4, self.window.get_height() * (5 + i)/20)\
                                                            , text_color= (200, 200, 200), text_background_color= (0, 0, 0))     
                self.window.blit( self.points, self.points_pos )                

        pygame.display.flip()

        self.clock = pygame.time.Clock()

    def run(self):
        """
        High Score loop
        """

        while not self.handle_events():
            
            self.clock.tick(20)

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
