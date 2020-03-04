import pygame as pg
from abc import ABC, abstractmethod

#Abstract paddle class
class Paddle(pg.sprite.Sprite, ABC):
    """paddle class"""

    def __init__( self, *, pos, score ):
        """ 
        Paddle constructor. 
        
        :param pos: starting position of the paddle
        :param move_up_button: ASCII of button responsible for moving up
        :param move_down_button: ASCII of button responsible for moving down
        """
        pg.sprite.Sprite.__init__( self, self.containers ) #call Sprite initializer
        screen = pg.display.get_surface()
        self.screen_rect = screen.get_rect()

        self.image = pg.Surface([ self.screen_rect.width * 1/64 , self.screen_rect.height * 1/9]).convert()
        self.image.fill((200, 200, 200))
        self.rect = self.image.get_rect( center = pos )

        self.speed = 10

        self.score = score #object of class score

    @abstractmethod
    def move(self): 
        pass
        

class Player_paddle(Paddle):

    def __init__( self, *, pos, score, move_up_button, move_down_button ):
        Paddle.__init__(self, pos = pos, score = score) #call Sprite initializer

        self.move_up_button = move_up_button # buttons responsible for moving in the right direction
        self.move_down_button = move_down_button

    def move(self, pressed):
        """detect if move button for specific paddle was pressed""" 
        direction = pressed[ self.move_down_button ] - pressed[ self.move_up_button ]
        self.rect.move_ip( 0, direction * self.speed)
        self.rect = self.rect.clamp( self.screen_rect )# Don't let paddle go out of the screen

class Environment_paddle(Paddle):

    def __init__( self, *, pos, score ):
        Paddle.__init__(self, pos = pos, score = score) #call Sprite initializer

    def move(self, balls):
        for ball in balls:
            # Computer palette movement
            if ball.velocity[0] > 0:
                screen_rect = self.screen_rect
                if ball.rect.centerx < screen_rect.centerx:
                    if ball.rect.centery < self.rect.centery and self.rect.centery > screen_rect.height * 2/3 :
                        self.rect.move_ip( 0, -self.speed ) 
                    elif ball.rect.centery > self.rect.centery and self.rect.centery < screen_rect.height * 1/3:
                        self.rect.move_ip( 0, self.speed ) 
                else:
                    if ball.rect.centery < self.rect.centery + self.rect.height/4  :
                        self.rect.move_ip( 0, -self.speed ) 
                    elif ball.rect.centery > self.rect.centery - self.rect.height/4 :
                        self.rect.move_ip( 0, self.speed )

                self.rect = self.rect.clamp( screen_rect )# Don't let paddle go out of the screen