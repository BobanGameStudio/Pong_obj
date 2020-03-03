import pygame as pg
from pygame.locals import *
import sys
import os
import os.path

from button import Button
from load import make_text
from game import Game
from options import Options
from high_score import High_Score
from contact import Contact

if not pg.font: print ('Warning, fonts disabled')
if not pg.mixer: print ('Warning, sound disabled')

class Main_Menu(object):
    """
    Main menu. 
    """
    def __init__(self):
        """
        Main menu constructor.
        """
        pg.init()

        #Create display window
        infoObject = pg.display.Info() # Gets information about the screen
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % ( 0, 0 ) # The initial position of the window on the screen
        self.window = pg.display.set_mode(( infoObject.current_w, infoObject.current_h)) # Creating a game window
        pg.display.set_caption("Pong game") # Name of the game window

        #Create background surface
        self.background = pg.Surface( self.window.get_size() ).convert()
        self.background.fill( (0, 0, 0) )

        #Create main menu text
        self.text_menu, self.text_menu_pos = make_text( text= "PONG GAME", font_name= 'casio-fx-702p\casio-fx-702p.ttf'\
                                                    , size= 70, pos= (self.window.get_width()/2, self.window.get_height() * 3/20)\
                                                    , text_color= (200, 200, 200), text_background_color= (0, 0, 0))

        #Create menu images
        img_folder = "main_menu_buttons"
        self.buttons = {
                "button_start_PvP" : None ,
                "button_start_PvE" : None,
                "button_options" : None,
                "button_high_score" : None,
                "button_contact" : None,
                "button_exit" : None,
                }
            #Buttons possition
        first_button_pos = ( self.window.get_width()/2, self.window.get_height() * 3/10)
        button_spacing = self.window.get_height() * 2/20

        all_buttons = []
        for i, button_name in enumerate( self.buttons ):
            self.buttons[button_name] = ( Button(folder_name = img_folder, \
                                            img_name = button_name, pos = (first_button_pos[0], first_button_pos[1] + button_spacing * i) ) )
            all_buttons.append ( self.buttons[button_name] )

        self.allsprites = pg.sprite.RenderPlain( all_buttons )

        self.choosed_option = [False, False, False, False, False, False]

        #Clock initialization
        self.clock = pg.time.Clock()

        self.click_down = False
        self.click_up = False
        
    def run(self):
        """
        Main menu loop
        """
        while not self.handle_events():
            # operate in a loop until you receive a signal to exit
            mx, my = pg.mouse.get_pos()

            self.clock.tick(60)

            self.window.blit( self.background, (0, 0))
            self.window.blit( self.text_menu, self.text_menu_pos )

            self.allsprites.update()
            self.allsprites.draw( self.window )

            for i, button_name in enumerate( self.buttons ):
                if self.buttons[button_name].rect.collidepoint( ( mx, my ) ):
                    if self.click_down == True:
                        self.buttons[button_name].push()
                    elif self.click_up == True:
                        self.choosed_option[i] = True
                        # selected_option = self.game_windows[i]
                        # if selected_option != True:
                        #     selected_option_obj = selected_option( self.window )
                        #     selected_option_obj.run()
                        # else:
                        #     return True
                        # del selected_option_obj
                    else:
                        self.buttons[button_name].release()
                else:
                    self.buttons[button_name].release()
            for opt_num, opt in enumerate( self.choosed_option ):
                if opt == True:
                    if opt_num == 0:
                        game = Game(self.window, "pvp")
                        game.run()
                        del game
                    elif opt_num == 1:
                        game = Game(self.window, "pve")
                        game.run()
                        del game
                    elif opt_num == 2:
                        options = Options(self.window)
                        options.run()
                        del options
                    elif opt_num == 3:
                        high_score =High_Score(self.window)
                        high_score.run()
                        del high_score
                    elif opt_num == 4:
                        contact = Contact(self.window)
                        contact.run()
                        del contact
                    elif opt_num == 5:
                        return True
                    self.choosed_option[opt_num] = False
            pg.display.flip()

        pg.quit()
        sys.exit() 

    def handle_events(self):
        """
        Handling system events

        :return True if pg reported a quit event
        """
        self.click_up = False
        for event in pg.event.get():
            if event.type == pg.locals.QUIT:
                return True
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.click_down = True
            elif event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    self.click_up = True
                    self.click_down = False