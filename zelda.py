'''
ZELDA 2D DUNGEON GAME
This is intended to be a Zelda top down dungeon crawler
Hopefully will have puzzles and chests and enemies and a boss.

'''

from Game import *
game = Game()

while True:
    game.event_loop()
    game.get_input()
    
    #font_surf = font.render(text, True, red) # the text to render, then whether or not to antialias, then the text color
        # the fond.render() fxn returns a seperate surface
        # so we need to blit this surface to the screen
    
    game.draw()
    game.move()
    #print(f"Player health: {game.player.health}")
    pygame.display.update()
    clock.tick(FPS)