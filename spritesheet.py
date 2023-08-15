from fund_values import *

decor_spritesheet = pygame.image.load("./sprites/decor.png")

#screen.blit(decor_spritesheet, (WIDTH/2, HEIGHT/2))
SPRITE_WIDTH = 24

# make a surface to draw individual images on
image_surf = pygame.Surface((SPRITE_WIDTH, SPRITE_WIDTH)).convert_alpha() # convert alpha is to optimize pic quality in png
    
# blit the image you want on the image surface, 2nd param is place to blit on the new surface (image_surf) 
#   and 3rd is area including two coords of the top left corner to bottom right corner of the image from the spritesheet
image_surf.blit(decor_spritesheet, (0, 0), (0, 0, SPRITE_WIDTH, SPRITE_WIDTH))
    
# scale the image up
scale_factor = 3
image_surf = pygame.transform.scale(image_surf, (SPRITE_WIDTH * scale_factor, SPRITE_WIDTH * scale_factor))

# display the image surface
screen.blit(image_surf, (WIDTH/2, HEIGHT/2))