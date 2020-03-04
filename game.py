import pygame as pg
from pygame.locals import *

from load import make_text
from paddle import Player_paddle, Environment_paddle
from ball import Ball
from fps import Fps
from score import Score
from high_score import save_result

class Game(object):
    def __init__(self, window, game_mode):
        """
        Game constructor.
        """
        self.window = window
        self.window_rect = window.get_rect()

        #Creating a bacground of game
        self.background = pg.Surface( self.window.get_size() ).convert()
        self.background.fill( (0, 0, 0) )
        bg_strip = pg.Surface([self.window.get_width() * 1/128, self.window.get_height() * 1/40]).convert()
        bg_strip.fill((200, 200, 200))
        strip_pos = bg_strip.get_rect( center = ( self.window.get_width()/2, self.window.get_height() * 1/40 )) 
        strip_distance = self.window.get_height() * 1/40

        for i in range(0,20):
            self.background.blit( bg_strip, ( strip_pos[0], strip_pos[1] + i * (strip_distance + bg_strip.get_height() ) ))

        self.window.blit(self.background, (0, 0))
        pg.display.flip()

        if pg.font:
            self.text_menu, self.text_menu_pos = make_text( text= "game_section", font_name= 'casio-fx-702p\casio-fx-702p.ttf'\
                                                        , size= 70, pos= (self.window.get_width()/2, self.window.get_height() * 3/20)\
                                                        , text_color= (200, 200, 200), text_background_color= (0, 0, 0))
        
        # Initialize Game Groups
        self.all_paddles = pg.sprite.Group()
        self.p_paddles = pg.sprite.Group()
        self.e_paddles = pg.sprite.Group()
        self.balls = pg.sprite.Group()
        self.fps_group = pg.sprite.Group()
        self.score = pg.sprite.Group()
        self.all = pg.sprite.RenderUpdates() 
    
        # assign default groups to each sprite class
        Player_paddle.containers = self.all_paddles, self.p_paddles , self.all
        Environment_paddle.containers = self.all_paddles, self.e_paddles , self.all
        Ball.containers = self.balls, self.all
        Fps.containers = self.fps_group
        Score.containers = self.score, self.all
    
        #region initiate balls
        number_of_balls = 1
        for i in range( 0, number_of_balls ):
            Ball( start_pos = (self.window.get_width()/2, self.window.get_height() * 1/3 + i * self.window.get_height() * 1/40),\
                 x_start_speed = 5, y_start_speed = 5 if i%2 == 0 else  -10   )
        #endregion

        #region initiate players
        number_of_players = 2

        if number_of_players >= 1:
            Player_paddle( pos= ( self.window.get_width() * 1/30, self.window.get_height()/2 ), score = Score( (self.window_rect.right * 1/3, self.window_rect.bottom * 1/10) )\
                                , move_up_button= 119, move_down_button= 115, )
        if number_of_players >= 2:
            if game_mode == "pvp":
                Player_paddle( pos= ( self.window.get_width() * 29/30, self.window.get_height()/2 ), score = Score( (self.window_rect.right * 2/3, self.window_rect.bottom * 1/10) )\
                                , move_up_button= 273, move_down_button= 274, )
            elif game_mode == "pve":
                Environment_paddle( pos= ( self.window.get_width() * 29/30, self.window.get_height()/2 ), score = Score( (self.window_rect.right * 2/3, self.window_rect.bottom * 1/10) ))
        if number_of_players >= 3:
            Player_paddle( pos= ( self.window.get_width() * 22/30, self.window.get_height()/2 ), move_up_button= 119, move_down_button= 115, score = Score( (self.window_rect.x * 1/3, self.window_rect.y * 5/10)), mode = "player" )
        if number_of_players >= 4:
            Player_paddle( pos= ( self.window.get_width() * 1/30, self.window.get_height()/2 ), move_up_button= 273, move_down_button= 274, score = Score( (self.window_rect.x * 1/3, self.window_rect.y * 8/10) ), mode = "player" )
        #endregion 
        
        #initiate fps
        self.fps = Fps()
    
        #set mouse invisible
        pg.mouse.set_visible(0)
        #initiate time in game
        self.clock = pg.time.Clock()

    def run(self):
        """
        Game loop
        """
    
        while not self.handle_events():
            
            self.all.clear(self.window, self.background)
            self.all.update()

            for paddle in self.e_paddles:
                paddle.move( self.balls )
            for ball in self.balls:
                ball.paddle_collide( self.all_paddles )
            self.fps.current_fps( self.clock )

            dirty = self.all.draw(self.window)
            
            pg.display.update(dirty)
            
            self.clock.tick(50)         

    def handle_events(self):
        """
        Handling system events

        :return True if pygame reported a quit event
        """
        for event in pg.event.get():
            if event.type == pg.locals.QUIT:
                pg.quit()
                sys.exit()
                save_result(self.p_paddles.sprites()[0].score.current_score - self.e_paddles.sprites()[0].score.current_score)
                return True
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                pg.mouse.set_visible(1)
                save_result(self.p_paddles.sprites()[0].score.current_score - self.e_paddles.sprites()[0].score.current_score)
                return True
            if event.type == KEYDOWN and event.key == K_F1:
                self.fps.reverse_visibility( self.all )
                

        pressed = pg.key.get_pressed()

        for player in self.p_paddles:
            player.move( pressed )
