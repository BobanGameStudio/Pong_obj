import pygame as pg
from pygame.locals import *

from load import make_text

class Contact(object):
    def __init__(self, window, small_window):
        """
        Game constructor.
        """
        self.window = window

        self.background = pg.Surface( self.window.get_size() )
        self.background = self.background.convert()
        self.background.fill( (0, 0, 0) )

        if small_window:
            font_size = 40
        else:
            font_size = 70
        if pg.font:
            self.text_contact_title, self.text_contact_title_pos = make_text( text= "CONTACT WITH ME:", font_name= 'casio-fx-702p\casio-fx-702p.ttf'\
                                                        , size= font_size, pos= (self.window.get_width()/2, self.window.get_height() * 4/20)\
                                                        , text_color= (200, 200, 200), text_background_color= (0, 0, 0))
            self.text_contact_BGS, self.text_contact_BGS_pos = make_text( text= "Boban Games Studio", font_name= r'times new roman\times new roman.ttf'\
                                                        , size= font_size, pos= (self.window.get_width()/2, self.window.get_height() * 8/20)\
                                                        , text_color= (200, 200, 200), text_background_color= (0, 0, 0))
            self.text_contact_mail, self.text_contact_mail_pos = make_text( text= "boban.skolimowski@gmail.com", font_name= r'times new roman\times new roman.ttf'\
                                                        , size= font_size, pos= (self.window.get_width()/2, self.window.get_height() * 1/2)\
                                                        , text_color= (200, 200, 200), text_background_color= (0, 0, 0))

        self.clock = pg.time.Clock()

    def run(self):
        """
        Contact loop
        """

        while not self.handle_events():
            self.clock.tick(60)
            
            self.background.blit( self.text_contact_title, self.text_contact_title_pos )
            self.background.blit( self.text_contact_BGS, self.text_contact_BGS_pos )
            self.background.blit( self.text_contact_mail, self.text_contact_mail_pos )
            self.window.blit( self.background, (0, 0))

            pg.display.flip()
            

    def handle_events(self):
            """
            Handling system events

            :return True if pg reported a quit event
            """
            for event in pg.event.get():
                if event.type == pg.locals.QUIT:
                    pg.quit()
                    sys.exit()
                    return True
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    return True
