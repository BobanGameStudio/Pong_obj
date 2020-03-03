import pygame as pg
import time

class Ball(pg.sprite.Sprite):
    """Ball class"""

    def __init__(self, *, start_pos, x_start_speed = 5, y_start_speed = 5):
        """ 
        Ball constructor. 

        :param start_pos: starting position of the ball
        :param x_start_speed: starting x speed 
        :param y_start_speed: starting y speed 
        """
        pg.sprite.Sprite.__init__(self, self.containers) #call Sprite initializer
        screen = pg.display.get_surface()
        self.area = screen.get_rect()

        self.image = pg.Surface([ self.area.width * 1/100 , self.area.width * 1/100]).convert()
        self.image.fill((200, 200, 200))

        self.start_pos = start_pos
        self.rect = self.image.get_rect()
        self.set_pos( self.start_pos )

        self.speed_multiplier = 2

        self.start_velocity = [ x_start_speed, y_start_speed ]
        self.set_velocity( self.start_velocity )

        self.colided = False

    def set_pos(self, pos):
        self.rect.center = pos

    def set_velocity(self, vel):
        self.velocity = [ vel[0] * self.speed_multiplier, vel[1] * self.speed_multiplier ]

    def update(self):
        """move paddle in indicated direction"""
        self.rect.move_ip( self.velocity )

        #bounce if ball hit bottom or top
        if self.rect.top < self.area.top:
            self.rect.top = self.area.top - self.rect.top
            self.bounce_y()
        elif self.rect.bottom > self.area.bottom:
            self.rect.bottom = self.area.bottom - ( self.rect.bottom - self.area.bottom )
            self.bounce_y()
    
    def paddle_collide(self, paddles):
        if not self.colided:
            for paddle in pg.sprite.spritecollide( self, paddles, 0):#for all collided paddles
                if self.velocity[0] > 0:
                    shift_x = self.rect.right - paddle.rect.left
                else:
                    shift_x = self.rect.left - paddle.rect.right
                if self.velocity[1] > 0: 
                    shift_y = self.rect.bottom - paddle.rect.top
                else:
                    shift_y = self.rect.top - paddle.rect.bottom
                
                #bounce from the long edge
                if shift_x * self.velocity[0] <= shift_y * self.velocity[1]:
                    shift_y = round( self.velocity[1]/self.velocity[0] * shift_x )
                #bounce from the short edge
                else:
                    shift_x = round( self.velocity[0]/self.velocity[1] * shift_y )
                    self.bounce_y()

                self.rect.move_ip( -shift_x, -shift_y )
                self.bounce_x()
        
        if self.rect.right > self.area.right:
            for paddle in paddles:
                if paddle != paddles.sprites()[1]:
                    paddle.score.add_point()
            self.reset()
        elif self.rect.left < self.area.left:
            for paddle in paddles:
                if paddle != paddles.sprites()[0]:
                    paddle.score.add_point()
            self.reset()

    def bounce_x(self):
        """Inverts the velocity vector in the X axis"""
        self.velocity[0] *= -1

    def bounce_y(self):
        """Inverts the velocity vector in the Y axis"""
        self.velocity[1] *= -1

    def reset(self):
        """Sets the ball to the start position and reverses the velocity vector in the X axis"""
        self.set_pos( self.start_pos )
        self.bounce_x()
        ball_speed_x = ( 1 if self.velocity[1] >= 0 else -1 ) * self.start_velocity[0]
        ball_speed_y = ( 1 if self.velocity[1] >= 0 else -1 ) * self.start_velocity[1]
        self.set_velocity( [ ball_speed_x, ball_speed_y ] )
