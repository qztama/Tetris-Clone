import pygame, sys, random
import piece, Game

BLOCK_SIZE = 40
WIN_WIDTH = 20*BLOCK_SIZE
WIN_HEIGHT = 23*BLOCK_SIZE
SCREEN_WIDTH = 10
SCREEN_HEIGHT = 20

pygame.init()

#creating the board

window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
window.fill((150,150,150))

pygame.display.set_caption('Tetris')

running = True

while running:
    game = Game.Game(BLOCK_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT, WIN_WIDTH, WIN_HEIGHT, window)

    running = game.run_game()

    if running:
        key_entered = False

        while not key_entered:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    key_entered = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False
                    key_entered = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    del game
                    key_entered = True

print('Done')
