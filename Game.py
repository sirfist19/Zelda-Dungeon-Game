from Skeleton import *
from Player import *
from Tilemap import Tilemap
from Map import Map
from Tiles import *

class UI:
    def __init__(self, player):
        self.font = pygame.font.Font(None, 36)
        self.game_over_font = pygame.font.Font(None, 130)
        self.player = player
        self.name_text = "Name: " 
        self.health_text = "Health: " 
        self.offset = 20
        self.seperation_text = "     "
        self.game_over_text = "GAME OVER!"

    def get_ui_text(self):
        name_section = self.name_text + self.player.name
        health_section = self.health_text + str(self.player.health) + "/" + str(self.player.max_health)
        return name_section + self.seperation_text + health_section 
    
    def draw_game_over_screen(self):
        game_over_ui_surf = self.game_over_font.render(self.game_over_text, True, red)  # Text, antialiasing, color
        screen.blit(game_over_ui_surf, (WIDTH/4, HEIGHT/2 - 50))

    def draw(self):
        #ui_text = self.name_text + self.seperation_text + self.health_text
        health_ui_surf = self.font.render(self.get_ui_text(), True, red)  # Text, antialiasing, color
        screen.blit(health_ui_surf, (self.offset, self.offset))

class Game:
    def __init__(self):
        self.screen = screen
        self.bg_color = black
        self.player = Player()
        self.ui = UI(self.player)
        self.game_over = False
        self.map = Map()
        self.tilemap = Tilemap(self.map.cur_room.tiles)

    def get_input(self):
        if self.player:
            keys = pygame.key.get_pressed()
            if self.player.moving_dir != Direction.NOT_MOVING:
                self.player.prev_moving_dir = self.player.moving_dir

            if keys[pygame.K_w]:
                self.player.moving_dir = Direction.UP
            elif keys[pygame.K_a]:
                self.player.moving_dir = Direction.LEFT
            elif keys[pygame.K_s]:
                self.player.moving_dir = Direction.DOWN
            elif keys[pygame.K_d]:
                self.player.moving_dir = Direction.RIGHT
            else:
                self.player.moving_dir = Direction.NOT_MOVING 

            if keys[pygame.K_RETURN]:
                self.player.is_attacking = True   
            else:
                self.player.is_attacking = False
    
    def event_loop(self):
        # pygame.event is a list of events to sort through each frame
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        
        self.is_alive_check() # removes any dead enemies or the player
        self.collision_check()

    def is_alive_check(self):
        self.map.cur_room.enemy_alive_check()
        
        if self.player and not self.player.is_alive():
            print("Game Over")
            self.game_over = True
            self.player = None

    def collision_check(self):
        # Player vs enemy collisions
        for enemy in self.map.cur_room.enemies:
            if self.player:
                if self.player.hitbox.colliderect(enemy.hitbox):
                    self.player.damage(enemy.attack)
                    enemy.damage(self.player.attack)
                    
                if self.player.sword.rect.colliderect(enemy.hitbox):
                    print("Sword collided with the enemy")
                    enemy.damage(self.player.sword.attack)
            #print(f"enemy: {enemy.health}")

        # Check for tilemap collisions like walls, pits, doors etc.
        for i in range(len(self.tilemap.cur_room_tiles)):
            for j in range(len(self.tilemap.cur_room_tiles[0])):
                tile = self.tilemap.cur_room_tiles[i][j]
                if type(tile) == Wall:
                    if self.player and self.player.hitbox.colliderect(tile.get_rect(j,i)):
                        player_center = self.player.hitbox.center
                        wall_center = tile.get_rect(j,i).center
                        self.player.wall_bounce(player_center, wall_center)

                    for enemy in self.map.cur_room.enemies:
                        if enemy.hitbox.colliderect(tile.get_rect(j,i)):
                            enemy_center = enemy.hitbox.center
                            wall_center = tile.get_rect(j,i).center
                            enemy.wall_bounce(enemy_center, wall_center)
                if type(tile) == UpDoor:
                    if self.player and self.player.hitbox.colliderect(tile.get_rect(j,i)):
                        self.map.cur_room = self.map.cur_room.get_north_room()
                        self.tilemap.set_new_cur_room_tiles(self.map.cur_room.tiles)
                        print("Went up a room")
                        self.player.spawn_at_south_door()
                if type(tile) == DownDoor:
                    if self.player and self.player.hitbox.colliderect(tile.get_rect(j,i)):
                        self.map.cur_room = self.map.cur_room.get_south_room()
                        self.tilemap.set_new_cur_room_tiles(self.map.cur_room.tiles)
                        self.player.spawn_at_north_door()
                if type(tile) == LeftDoor:
                    if self.player and self.player.hitbox.colliderect(tile.get_rect(j,i)):
                        self.map.cur_room = self.map.cur_room.get_west_room()
                        self.tilemap.set_new_cur_room_tiles(self.map.cur_room.tiles)
                        self.player.spawn_at_east_door()
                if type(tile) == RightDoor:
                    if self.player and self.player.hitbox.colliderect(tile.get_rect(j,i)):
                        self.map.cur_room = self.map.cur_room.get_east_room()
                        self.tilemap.set_new_cur_room_tiles(self.map.cur_room.tiles)
                        self.player.spawn_at_west_door()
        #print(self.map, self.map.cur_room)

    def draw(self):
        screen.fill(self.bg_color)
        self.tilemap.draw()
        
        for enemy in self.map.cur_room.enemies:
            enemy.draw()
        if self.player:
            self.player.draw()
        self.ui.draw()

        if self.game_over:
            self.ui.draw_game_over_screen()
        #draw_point(4,4)

    def move(self):
        if self.player:
            self.player.move()

        for enemy in self.map.cur_room.enemies:
            enemy.move()
            #print(enemy.moving_dir)
            enemy.patrol()
    
    
