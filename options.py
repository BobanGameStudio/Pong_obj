import pygame
from pygame.locals import *
from button import Button
import math

from load import load_image

def unicode_from_number( number ):
    """ Give unicode from ascii for the chosen ones """
    if number == 0:# klawisz 
        return ("_")
    if number == 1:# klawisz 
        return ("")
    if number == 9:# klawisz 'TAB'
        return ("TAB")
    if number == 12:# klawisz 'ENTER'
        return ("ENTER")
    if number == 32:# klawisz 'SPACE'
        return ("SPACE")
    if number == 39:# klawisz '''
        return pygame.key.name( number )
    if number >= 44 and number <= 57:# klawisze ',' '-' '.' '/' '0 - 9'
        return pygame.key.name( number )
    if number == 59:# klawisz ';'
        return pygame.key.name( number )
    if number == 61:# klawisz '='
        return pygame.key.name( number )
    if number >= 97 and number <= 122:# klawisze 'a - z' i 'A - Z'
        return pygame.key.name( number )
    if number == 273:# klawisz 'UP'
        return ("UP")
    if number == 274:# klawisz 'DOWN'
        return ("DOWN")
    if number == 275:# klawisz 'RIGHT'
        return ("RIGHT")
    if number == 276:# klawisz 'LEFT'
        return ("LEFT")
    if number >= 282 and number <= 293:# klawisze 'F1 - F12'
        return ("F" + str( number - 281 ) )
    return ("_")

class Options(object):
    def __init__(self, window, options_sett, small_window):
        """
        Game constructor.
        """
        self.window = window
        self.options_sett = options_sett[:]
        self.arrow_right_state = [False, False, False]
        self.arrow_left_state = [False, False, False]

        if pygame.font:
            self.GRAY = (200, 200, 200)
            self.DARK_GRAY = (50, 50, 50)
            self.BLACK = (0, 0, 0)

            #region create background text
            font_menu = pygame.font.Font('fonts/casio-fx-702p.ttf', 70)#
            self.text_menu = font_menu.render( "options", 1, self.GRAY, self.BLACK )
            self.text_menu_pos = self.text_menu.get_rect( centerx = self.window.get_width()/2, \
                                                            centery = self.window.get_height() * 3/20 )
            
            if small_window:
                font_options = pygame.font.Font('fonts/casio-fx-702p.ttf', 20)# Font of all options names
            else:
                font_options = pygame.font.Font('fonts/casio-fx-702p.ttf', 40)# Font of all options names
            self.text_options_names = [  font_options.render( "Ball speed", 1, self.GRAY, self.BLACK ),
                                        font_options.render( "Paddle speed", 1, self.GRAY, self.BLACK ),
                                        font_options.render( "Difficulty level", 1, self.GRAY, self.BLACK ),
                                        font_options.render( "Paddle up p.1", 1, self.GRAY, self.BLACK ),
                                        font_options.render( "Paddle down p.1", 1, self.GRAY, self.BLACK ),
                                        font_options.render( "Paddle up p.2", 1, self.GRAY, self.BLACK ),
                                        font_options.render( "Paddle down p.2", 1, self.GRAY, self.BLACK ),
                                        font_options.render( "Pause", 1, self.GRAY, self.BLACK ),
                                        font_options.render( "Show fps", 1, self.GRAY, self.BLACK )]

            self.first_option_pos = self.text_options_names[0].get_rect( centerx = self.window.get_width()*1/3, \
                                                                        centery = self.window.get_height() * 20/80 )
            #endregion

            #region create background
            self.background = pygame.Surface( self.window.get_size() )
            self.background = self.background.convert()
            self.background.fill( (0, 0, 0) )

            self.background.blit( self.text_menu, self.text_menu_pos )
            
            background_stripe = pygame.Surface([round(self.window.get_width()/10), round(self.window.get_height()/19)])
            background_stripe.fill(self.DARK_GRAY)
            background_stripe_pos = background_stripe.get_rect(centerx = self.window.get_width()*3/4,\
                                                                centery = self.window.get_height()*20/80)
            self.all_stripes = []
            for option_name_num, option_name in enumerate(self.text_options_names):
                self.background.blit( option_name, (self.first_option_pos[0], self.first_option_pos[1] + option_name_num * self.window.get_height()*5/80))
                if option_name_num > 2:
                    self.background.blit(background_stripe, (background_stripe_pos[0], background_stripe_pos[1] + option_name_num * self.window.get_height()*5/80))
                    self.all_stripes.append(background_stripe_pos.move(0, option_name_num * self.window.get_height()*5/80))
            self.stripes_update = [0 for i in range(0, 6)]
            self.stripe_time = 0
            #endregion
            

            #region load images(0, )
            self.stake_dist = round(self.window.get_width()/96)
            
            self.big_stake, self.big_stake_pos = load_image( "big_stake.png" )
            self.small_stake, self.small_stake_pos = load_image( "small_stake.png" )
            self.start_stake_pos1 = (self.window.get_width()*3/4 - background_stripe.get_width()/2,\
                                 self.window.get_height()*20/80 )
            self.start_stake_pos2 = (self.window.get_width()*3/4 - background_stripe.get_width()/2,\
                                 self.window.get_height()*20/80 + self.window.get_height()*5/80 )

            self.arrows =[] 
            if small_window:
                dist = 75
            else:
                dist = 140
            for i in range(0, 3):
                self.arrows.append(Button(folder_name = "", img_name = "button_left2", \
                                        pos = (self.window.get_width()*3/4 - dist, self.window.get_height() * 20/80 + i * self.window.get_height() * 5/80) ))
                self.arrows.append(Button(folder_name = "", img_name = "button_right2", \
                                        pos = (self.window.get_width()*3/4 + dist, self.window.get_height() * 20/80 + i * self.window.get_height() * 5/80) ))
            self.arrow_choosen = [False for i in range(0,6)]

            self.allsprites = pygame.sprite.RenderPlain( self.arrows )
            #endregion

            #region create easy, hard text
            self.text_easy = font_options.render( "easy", 1, self.GRAY, self.BLACK )
            self.text_easy_pos = self.text_easy.get_rect( centerx = self.window.get_width()*3/4, \
                                                            centery = self.window.get_height() * 20/80 + 2 * self.window.get_height()*5/80 )
            self.text_hard = font_options.render( "hard", 1, self.GRAY, self.BLACK )
            self.text_hard_pos = self.text_hard.get_rect( centerx = self.window.get_width()*3/4, \
                                                            centery = self.window.get_height() * 20/80 + 2 * self.window.get_height()*5/80 )
            #endregion
            
            #region create start pos for key sett
            self.key_sett_start_pos = ( self.window.get_width()*3/4, self.window.get_height() * 20/80 + 3 * self.window.get_height()*5/80 )
            if small_window:
                self.font_options_names = pygame.font.Font('fonts/casio-fx-702p.ttf', 20)
            else:
                self.font_options_names = pygame.font.Font('fonts/casio-fx-702p.ttf', 30)
            #endregion

            #region click down/up
            self.click_down = False
            self.click_up = False
            #endregion

        self.clock = pygame.time.Clock()

    def run(self):
        """
        Game loop
        """

        while not self.handle_events():
            mx, my = pygame.mouse.get_pos()
            self.clock.tick(50)
            
            self.window.blit( self.background, (0, 0))
            for stake_num in range(0, 10):# blit stakes
                if stake_num < self.options_sett[0]:# blit stakes for ball speed
                    self.big_stake_pos.center = ( self.start_stake_pos1[0] + stake_num * self.stake_dist, self.start_stake_pos1[1] )
                    self.window.blit( self.big_stake, self.big_stake_pos )
                else:
                    self.small_stake_pos.center = ( self.start_stake_pos1[0] + stake_num * self.stake_dist, self.start_stake_pos1[1] )
                    self.window.blit( self.small_stake, self.small_stake_pos )

                if stake_num < self.options_sett[1]:# blit stakes for paddle speed
                    self.big_stake_pos.center = ( self.start_stake_pos2[0] + stake_num * self.stake_dist, self.start_stake_pos2[1] )
                    self.window.blit( self.big_stake, self.big_stake_pos )
                else:
                    self.small_stake_pos.center = ( self.start_stake_pos2[0] + stake_num * self.stake_dist, self.start_stake_pos2[1] )
                    self.window.blit( self.small_stake, self.small_stake_pos )
            
            if self.options_sett[2] == "easy":# blit easy/hard text
                self.window.blit( self.text_easy, self.text_easy_pos )
            elif self.options_sett[2] == 'hard':
                self.window.blit( self.text_hard, self.text_hard_pos )
            
            for key_opt_num in range(0, 6):# create and blit key settings
                if self.stripes_update[key_opt_num] == 1:
                    if self.stripe_time < 30:
                        caption = self.font_options_names.render( unicode_from_number( 0 ), 1, self.GRAY, self.DARK_GRAY )
                        
                    elif self.stripe_time < 60:
                        caption = self.font_options_names.render( unicode_from_number( 1 ), 1, self.GRAY, self.DARK_GRAY )
                        
                    self.stripe_time += 1
                    if self.stripe_time == 60:
                            self.stripe_time = 0

                else:
                    caption = self.font_options_names.render( unicode_from_number( self.options_sett[3 + key_opt_num] ), 1, self.GRAY, self.DARK_GRAY )
                caption_pos = caption.get_rect( centerx = self.key_sett_start_pos[0], \
                                                centery = self.key_sett_start_pos[1] + key_opt_num * self.window.get_height()*5/80)
                self.window.blit(caption, caption_pos)
            
            self.allsprites.update()
            self.allsprites.draw( self.window )

            for arrow_num, arrow in enumerate( self.arrows ):
                if arrow.rect.collidepoint( ( mx, my ) ):
                    if self.click_down == True:
                        arrow.push()
                    elif self.click_up == True:
                        self.arrow_choosen[arrow_num] = True #option was choosed
                    else:
                        arrow.release()
                else:
                    arrow.release()
            
            for arrow_num, arrow in enumerate(self.arrow_choosen):# arrow support
                if arrow: 
                    if arrow_num%2 == 0:
                        if (arrow_num == 0 or arrow_num == 2) and self.options_sett[int(math.floor(arrow_num/2))] > 1:   
                            self.options_sett[int(math.floor(arrow_num/2))] -= 1   
                        elif arrow_num == 4 and self.options_sett[int(math.floor(arrow_num/2))] == "hard":
                            self.options_sett[int(math.floor(arrow_num/2))] = "easy"
                    elif arrow_num%2 == 1:
                        if (arrow_num == 1 or arrow_num == 3) and self.options_sett[int(math.floor(arrow_num/2))] < 10: 
                            self.options_sett[int(math.floor(arrow_num/2))] += 1
                        elif arrow_num == 5 and self.options_sett[int(math.floor(arrow_num/2))] == "easy":
                            self.options_sett[int(math.floor(arrow_num/2))] = "hard"
                    self.arrow_choosen[arrow_num] = False

                    self.save_options_to_file()
            
            for stripe_num, stripe in enumerate(self.all_stripes):
                if stripe.collidepoint( ( mx, my ) ):
                    if self.click_up:
                        self.stripes_update = [0 for i in range(0, 6)]
                        self.stripes_update[stripe_num] = 1

            pygame.display.flip()
        return self.options_sett[:]
    
    def save_options_to_file(self):
        #region saving changes into file
        file = open('options.txt','w')

        file.write( f'Ball speed:{self.options_sett[0]}\n')
        file.write( f'Paddle speed:{self.options_sett[1]}\n')
        
        if self.options_sett[2] == 'easy':
            file.write( f'Difficulty level:0\n')
        elif self.options_sett[2] == 'hard':
            file.write( f'Difficulty level:1\n')
        file.write(f'Gora gracz 1:{self.options_sett[3]}\n')
        file.write( f'Dol gracz 1:{self.options_sett[4]}\n')
        file.write( f'Gora gracz 2:{self.options_sett[5]}\n')
        file.write( f'Dol gracz 2:{self.options_sett[6]}\n')
        file.write( f'Pauza:{self.options_sett[7]}\n')
        file.write( f'ShowFps:{self.options_sett[8]}\n')
        file.close()
        #endregion

    def handle_events(self):
            """
            Handling system events

            :return True if pygame reported a quit event
            """
            self.click_up = False
            for event in pygame.event.get():
                if event.type == pygame.locals.QUIT:
                    pygame.quit()
                    sys.exit()
                    return True
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        return True
                    else:
                        if sum(self.stripes_update) > 0:
                            if event.key == 9 or event.key == 12 or event.key == 32 or event.key == 39 or ( event.key >= 44 and event.key <= 57 ) or event.key == 59  or event.key == 61 or ( event.key >= 97 and event.key <= 122 ) or ( event.key >= 273 and event.key <= 276 ) or ( event.key >= 282 and event.key <= 293 ):
                                if event.key not in self.options_sett or event.key == self.options_sett[self.stripes_update.index(1)+3]:
                                    self.options_sett[self.stripes_update.index(1)+3] = event.key
                                    self.save_options_to_file()
                                    self.stripes_update = [0 for i in range(0, 6)]

                elif event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.click_down = True
                elif event.type == MOUSEBUTTONUP:
                    if event.button == 1:
                        self.click_up = True
                        self.click_down = False
