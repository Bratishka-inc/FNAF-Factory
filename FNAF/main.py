import pygame

pygame.init()
(screen_width, screen_height) = (800, 600)
screen = pygame.display.set_mode((screen_width, screen_height))

#from core import Game
#game = Game()
import core
game = core.Game()
done = False
while done == False:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    game.flip()
    pygame.display.flip() # бновляет вывод на экран






pygame.quit()
