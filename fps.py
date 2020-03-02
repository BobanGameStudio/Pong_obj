import pygame as pg
from load import load_font

class Fps(pg.sprite.Sprite):
    """fps class"""

    def __init__(self):
        """ 
        fps constructor. 
        """
        pg.sprite.Sprite.__init__(self, self.containers)
        self.font = load_font(font_name = 'casio-fx-702p\casio-fx-702p.ttf', size = 10)
        self.color = (200,200,200)
        self.background_color = (0,0,0)
        msg = "Fps:"
        self.fps = 0
        self.image = self.font.render(msg, 0, self.color, self.background_color )
        self.rect = self.image.get_rect( topright = (pg.display.get_surface().get_rect().topright[0] * 24/25, 2) )
        
        self.visible = False
        
    def update(self):
        if self.visible:
            msg = "Fps: %d" % self.fps
            self.image = self.font.render(msg, 0, self.color, self.background_color )

    def current_fps(self, clock):
        self.fps = clock.get_fps()

    def reverse_visibility(self, group):
        self.visible = not self.visible
        if self.visible:
            group.add( self )
        else:
            group.remove( self )

    

