import pygame as pg
from load import load_font

class Score(pg.sprite.Sprite):
    """fps class"""

    def __init__(self, pos ):
        """ 
        fps constructor. 
        """
        pg.sprite.Sprite.__init__(self, self.containers)
        self.font = load_font(font_name = 'casio-fx-702p\casio-fx-702p.ttf', size = 70)
        self.color = (200,200,200)
        self.background_color = (0,0,0)
        self.last_score = -1
        self.current_score = 0
        self.update()
        self.rect = self.image.get_rect( center = pos ) 
    

    def update(self):
        if self.last_score != self.current_score:
            self.lastscore = self.current_score
            msg = "%d" % self.current_score
            self.image = self.font.render(msg, 0, self.color, self.background_color)

    def add_point(self):
        self.current_score += 1

