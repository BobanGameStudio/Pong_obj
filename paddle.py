import pygame as pg

class Paddle(pg.sprite.Sprite):
    """paddle class"""

    def __init__(self, *, pos, move_up_button = 119, move_down_button = 115, score, mode):
        """ 
        Paddle constructor. 
        
        :param pos: starting position of the paddle
        :param move_up_button: ASCII of button responsible for moving up
        :param move_down_button: ASCII of button responsible for moving down
        """
        pg.sprite.Sprite.__init__(self, self.containers) #call Sprite initializer
        screen = pg.display.get_surface()
        self.area = screen.get_rect()

        self.image = pg.Surface([ self.area.width * 1/64 , self.area.height * 1/9]).convert()
        self.image.fill((200, 200, 200))
        self.rect = self.image.get_rect( center = pos )

        self.move_up_button = move_up_button # buttons responsible for moving in the right direction
        self.move_down_button = move_down_button
        
        self.mode = mode

        self.speed = 10

        self.score = score #object of class score
    
    def follow_the_ball(self, balls):
        for ball in balls:
            # Computer palette movement
            if ball.velocity[0] > 0:
                disp_rect = pg.display.get_surface().get_rect()
                if ball.rect.centerx < disp_rect.centerx:
                    if ball.rect.centery < self.rect.centery and self.rect.centery > disp_rect.height * 2/3 :
                        self.rect.move_ip( 0, -self.speed ) 
                    elif ball.rect.centery > self.rect.centery and self.rect.centery < disp_rect.height * 1/3:
                        self.rect.move_ip( 0, self.speed ) 
                else:
                    if ball.rect.centery < self.rect.centery + self.rect.height/4  :
                        self.rect.move_ip( 0, -self.speed ) 
                    elif ball.rect.centery > self.rect.centery - self.rect.height/4 :
                        self.rect.move_ip( 0, self.speed )

                self.rect = self.rect.clamp( disp_rect )# Don't let paddle go out of the screen

    def move(self, pressed, window_rect ): 
        """detect if move button for specific paddle was pressed""" 
        direction = pressed[ self.move_down_button ] - pressed[ self.move_up_button ]
        self.rect.move_ip( 0, direction * self.speed)
        self.rect = self.rect.clamp( window_rect )# Don't let paddle go out of the screen
