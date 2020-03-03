import pygame as pg

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

    def update(self, paddles):
        """move paddle in indicated direction"""
        #self.rect.move_ip(self.velocity[0], self.velocity[1])

        dy, rest = 0, 0

        abs_vel = [abs(ele) for ele in self.velocity]
        abs_greater_index = abs_vel.index( max( abs_vel ) )
        abs_smaller_index = 0 if abs_greater_index == 1 else 1
        ball_speed_x = self.start_velocity[0]
        ball_speed_y = self.start_velocity[1]
        
        for i in range( 0, round( abs( self.velocity[0] ) ) ):
            #print( i, " ", self.velocity, " x, y: ", self.rect.x, " ", self.rect.y)

            d1 = self.velocity[ abs_greater_index ]/ abs(self.velocity[ abs_greater_index ] )
            d2, rest = divmod( self.velocity[ abs_smaller_index ]/abs( self.velocity[ abs_greater_index ] ) + rest, 1)
            
            #print(d1, d2, rest)
            if abs_greater_index == 0:
                self.rect.move_ip( d1, d2 )#move ball in new possition
            else:
                self.rect.move_ip( d2, d1 )#move ball in new possition
            d2 = rest

            #check collision between ball and paddle
            if not self.colided:
                for paddle in pg.sprite.spritecollide( self, paddles, 0):#for all collided paddles
                    if self.rect.left != paddle.rect.right - 1 and self.rect.right - 1 != paddle.rect.left:#if ball hit in short side of paddle
                        self.bounce_y()
                        ball_speed_x = 5
                        ball_speed_y = 5
                    else:
                        vel_sum = (abs(self.velocity[0]) + abs(self.velocity[1])) / self.speed_multiplier
                        ball_paddle_abs_pos = abs( self.rect.centery - paddle.rect.centery )
                        collision_area = ( paddle.rect.height/2 + self.rect.height )
                        ball_speed_x = round ( -self.velocity[0]/abs(self.velocity[0]) * ( 1 - ball_paddle_abs_pos/collision_area ) * vel_sum )
                        ball_speed_y = round ( ball_paddle_abs_pos/collision_area * vel_sum )
                          
                    self.bounce_x()
                    self.colided = True
        if self.colided:
            if len( pg.sprite.spritecollide( self, paddles, 0) ) == 0: #ball is not collided with any paddle
                self.colided = False
                for paddle in paddles:
                    if (paddle.rect.left < self.rect.right < paddle.rect.right) or (paddle.rect.left < self.rect.left < paddle.rect.right):
                        self.colided = True #Ball is not collided but still in paddle waist
                if self.colided == False:
                    print( [ ball_speed_x, ball_speed_y ] , " new vel" )
                    print( [ self.velocity[0], self.velocity[1] ], " vel")
                    self.set_velocity( [ ball_speed_x, ball_speed_y ] )

        if self.rect.top < self.area.top:
            self.rect.top = self.area.top - self.rect.top
            self.bounce_y()
        elif self.rect.bottom > self.area.bottom:
            self.rect.bottom = self.area.bottom - ( self.rect.bottom - self.area.bottom )
            self.bounce_y()
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
        #( -1 if self.velocity[1] >= 0 else 1 )
        ball_speed_x = ( -1 if self.velocity[1] >= 0 else 1 ) * self.start_velocity[0]
        ball_speed_y = ( 1 if self.velocity[1] >= 0 else -1 ) * self.start_velocity[1]
        self.set_velocity( [ ball_speed_x, ball_speed_y ] )
