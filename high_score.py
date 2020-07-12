import pygame
from pygame.locals import *
from load import make_text

class High_Score(object):
    def __init__(self, window, small_window):
        """
        High Score constructor.
        """
        self.window = window

        self.background = pygame.Surface( self.window.get_size() )
        self.background = self.background.convert()
        self.background.fill( (0, 0, 0) )

        self.window.blit( self.background, (0, 0))

        self.text_highscores, self.text_highscores_pos = make_text( text= "High scores", font_name= 'casio-fx-702p\casio-fx-702p.ttf'\
                                                            , size= 70, pos= (self.window.get_width()/2, self.window.get_height() * 3/20)\
                                                            , text_color= (200, 200, 200), text_background_color= (0, 0, 0))
        self.text_highscores_des, self.text_highscores_des_pos = make_text( text= "maximum difference between players points(only from pve)", font_name= 'casio-fx-702p\casio-fx-702p.ttf'\
                                                            , size= 15 if small_window else 25, pos= (self.window.get_width()/2, self.window.get_height() * (10/40 if small_window else 9/40))\
                                                            , text_color= (200, 200, 200), text_background_color= (0, 0, 0))

        self.window.blit( self.text_highscores, self.text_highscores_pos )
        self.window.blit( self.text_highscores_des, self.text_highscores_des_pos ) 
        
        with open( "highscores/High Scores.txt" ) as file:
            for i, wiersz in enumerate( file ):
                self.points, self.points_pos = make_text( text= "%.f" %int(wiersz), font_name= 'casio-fx-702p\casio-fx-702p.ttf'\
                                                            , size= 30, pos= (self.window.get_width()* 1/4, self.window.get_height() * (7 + i)/18)\
                                                            , text_color= (200, 200, 200), text_background_color= (0, 0, 0))     
                self.window.blit( self.points, self.points_pos )                

        pygame.display.flip()

        self.clock = pygame.time.Clock()

    def run(self):
        """
        High Score loop
        """

        while not self.handle_events():
            
            self.clock.tick(20)

    def handle_events(self):
            """
            Handling system events

            :return True if pygame reported a quit event
            """
            for event in pygame.event.get():
                if event.type == pygame.locals.QUIT:
                    pygame.quit()
                    sys.exit()
                    return True
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    return True

def save_result(result):
    results = []
    with open( "highscores/High Scores.txt" ) as file:
        for i, wiersz in enumerate( file ):
            results.append( int( wiersz ) )
    file.close()

    results.append( result )
    results = quick_sort( results )

    with open( "highscores/High Scores.txt", "w" ) as file:
        for i in range( 0, len(results)-1 ):
            file.write( str( results[i] ) + "\n" )

def quick_sort(list, descending = True):
    """ Quick sort for tuple, if optional argument is "True" then sort is descending, if "False" then ascending """
    if len(list) <= 1: #Jezeli na liscie do posortowania jest tylko jeden element zwroc go
        return list
    #Wybranie ostatniego elementu
    selected_item = ( list[ len(list)-1 ] )
    list = list[ 0:len(list)-1 ]#Usuniecie elementow z listy

    smaller = [ ]#Stworzenie list elementow mniejszych oraz wiekszych od wybranego
    bigger = [ ]
    
    for nr_elementu, element in enumerate(list):#Przydzielenie elementow do list w zaleznosci od tego czy sa smaller czy bigger od elementu wybranego
        if element < selected_item:
            #for i in range(0, len(list)):
            smaller.append(list[nr_elementu])
        else:
            #for i in range(0, len(list)):
            bigger.append(list[nr_elementu])
    
    smaller = quick_sort(smaller, descending)
    bigger = quick_sort(bigger, descending)

    if descending:
        result = bigger
        result.append(selected_item)
        result =  result + smaller
    else:
        result = smaller
        result.append(selected_item)
        result =  result + bigger
    
    return result