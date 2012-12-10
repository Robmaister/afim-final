'''
Created on Dec 7, 2012

@author: robert
'''

import pygame

STATE_INTRO = 0
STATE_GAME = 1
STATE_SCORE = 2

'''
def isSpecialTile(x, y):
    if (x == 0 and y in [3, 4, 5 ,6]) \
    or (x == 1 and y in [2, 3, 4, 5, 6, 7]) \
    or (x in [2, 4, 6, 7] and y in [1, 2, 3, 4, 5, 6, 7, 8]) \
    or (x == 3 and y in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]) \
    or (x == 5 and y in [1, 2, 4, 5, 7, 8]) \
    or (x in [8, 9] and y in [1, 2, 3, 6, 7, 8]):
        return True
    else:
        return False
   ''' 
    
def getTileRect(x, y):
    pos = (x, y)
    if pos in [(1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (1, 9), (4, 5), (7, 5), (6, 8), (6, 9)]:
        return pygame.rect.Rect((0, 0), (64, 64))
    elif pos in [(8, 4), (8, 5), (8, 6), (8, 7), (8, 8), (8, 9), (5, 5), (2, 5), (3, 8), (3, 9)]:
        return pygame.rect.Rect((64, 0), (64, 64))
    elif pos in [(4, 0), (5, 0), (3, 6), (6, 6)]:
        return pygame.rect.Rect((128, 0), (64, 64))
    elif pos in [(3, 4), (6, 4), (4, 7), (5, 7)]:
        return pygame.rect.Rect((192, 0), (64, 64))
    elif pos in [(4, 6), (7, 6)]:
        return pygame.rect.Rect((0, 128), (64, 64))
    elif pos in [(2, 6), (5, 6)]:
        return pygame.rect.Rect((64, 128), (64, 64))
    elif pos in [(4, 4), (7, 4), (6, 7), (1, 3)]:
        return pygame.rect.Rect((128, 128), (64, 64))
    elif pos in [(2, 4), (5, 4), (3, 7), (8, 3)]:
        return pygame.rect.Rect((192, 128), (64, 64))
    elif pos == (0, 3):
        return pygame.rect.Rect((0, 192), (64, 64))
    elif pos == (9, 3):
        return pygame.rect.Rect((64, 192), (64, 64))
    elif pos in [(3, 0), (2, 1), (1, 2)]:
        return pygame.rect.Rect((128, 192), (64, 64))
    elif pos in [(6, 0), (7, 1), (8, 2)]:
        return pygame.rect.Rect((192, 192), (64, 64))
    else:
        return pygame.rect.Rect((0, 64), (64, 64))
    

class Tileset(object):
    def __init__(self, path):
        lines = [line.rstrip() for line in open(path)]
        self.values = [[int(v) for v in line] for line in lines]
        
    def calculateScore(self, user_values):
        score = 0
        for i in range(10):
            for j in range(10):
                if self.values[i][j] == user_values[i][j]:
                    score += 1
        return score
        

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((640, 640))
    clock = pygame.time.Clock()
    exiting = False
    tile_values = Tileset("../assets/txt/base.txt")
    user_values = [[0 for j in range(10)] for i in range(10)]
    state = STATE_INTRO
    font = pygame.font.Font("../assets/fnt/PetMe.ttf", 36)
    intro_text_1 = font.render("Build a", False, (255, 255, 255))
    intro_text_2 = font.render("gingerbread house", False, (255, 255, 255))
    intro_text_3 = font.render("in 30 seconds!", False, (255, 255, 255))
    score_text_1 = font.render("Your score:", False, (255, 255, 255))
    gingerbread = pygame.image.load("../assets/img/gingerbreadtile.png").convert_alpha()
    background = pygame.image.load("../assets/img/background.png").convert_alpha()
    
    time = 0
    
    while not exiting:
        clock.tick(60)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                exiting = True
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    exiting = True
            elif e.type == pygame.MOUSEBUTTONDOWN:
                if state == STATE_INTRO:
                    state = STATE_GAME
                    pygame.time.set_timer(pygame.USEREVENT + 1, 30000)
                elif state == STATE_GAME:
                    x, y = pygame.mouse.get_pos()
                    x *= 0.015625 #divide by 64
                    y *= 0.015625
                    if e.button == 1:
                        user_values[int(y)][int(x)] = 1
                    elif e.button == 3:
                        user_values[int(y)][int(x)] = 0
            elif e.type == pygame.USEREVENT + 1:
                state = STATE_SCORE
        
        screen.fill((135, 206, 235))
        screen.blit(background, (0, 0))
        
        if state == STATE_INTRO:
            screen.blit(intro_text_1, (320 - intro_text_1.get_width() * 0.5, 200))
            screen.blit(intro_text_2, (320 - intro_text_2.get_width() * 0.5, 275))
            screen.blit(intro_text_3, (320 - intro_text_3.get_width() * 0.5, 350))
        elif state == STATE_GAME:
            time += clock.get_time()            
            for i, val_arr in enumerate(user_values):
                for j, val in enumerate(val_arr):
                    if val == 1:
                        screen.blit(gingerbread, (j * 64, i * 64), getTileRect(j, i))
                            
            #visible cursor
            x, y = pygame.mouse.get_pos()
            x *= 0.015625 #divide by 64
            y *= 0.015625
            screen.fill((159, 81, 41), pygame.rect.Rect((int(x) * 64, int(y) * 64), (64 ,64)), pygame.BLEND_MULT)
            
            #countdown timer
            screen.blit(font.render(str(30 - time / 1000), False, (255, 255, 255)), (0, 0))
            
        elif state == STATE_SCORE:
            screen.blit(score_text_1, (320 - score_text_1.get_width() * 0.5, 250))
            scoreSurf = font.render(str(tile_values.calculateScore(user_values)) + "/100", False, (255, 255, 255))
            screen.blit(scoreSurf, (320 - scoreSurf.get_width() * 0.5, 325))
        
        pygame.display.flip()