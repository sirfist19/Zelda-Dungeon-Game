from Enemy import *
from Player import *
from Tilemap import Tilemap
from Map import Map
from Tiles import *
from Items import *

class UI:
    def __init__(self, player):
        self.font = pygame.font.Font(None, 36)
        self.game_over_font = pygame.font.Font(None, 130)
        self.player = player
        self.name_text = "Name: " 
        self.health_text = "Health: " 
        self.key_text = "Keys: "
        self.gold_text = "Gold: "
        self.offset = 20
        self.seperation_text = "     "
        self.game_over_text = "GAME OVER!"

    def get_ui_text(self):
        name_section = self.name_text + self.player.name
        health_section = self.health_text + str(self.player.health) + "/" + str(self.player.max_health)
        key_section = self.key_text + str(self.player.keys)
        gold_section = self.gold_text + str(self.player.gold)
        ui_list = [name_section, health_section, key_section, gold_section]
        ui_list = [section + self.seperation_text for section in ui_list]
        return ''.join(ui_list)
    
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
        self.map = Map(CURRENT_LEVEL) 
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

            if keys[pygame.K_e]:
                self.player.e_pressed = True
            else:
                self.player.e_pressed = False
    
    def event_loop(self):
        # pygame.event is a list of events to sort through each frame
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        
        self.is_alive_check() # removes any dead enemies or the player
        self.collision_check()
        self.decrease_iFrames()
        self.item_actions()
    
    def decrease_iFrames(self):
        # decrease iFrames for all entities (player and enemies in cur room)
        #print(self.map.cur_room.enemies)
        for enemy in self.map.cur_room.enemies:
            enemy.decrease_iFrames()
        if self.player:
            self.player.decrease_iFrames()

    def is_alive_check(self):
        self.map.cur_room.enemy_alive_check()
        
        if self.player and not self.player.is_alive():
            print("Game Over")
            self.game_over = True
            self.player = None

    def player_enemy_collisions(self):
        # Player vs enemy collisions
        for enemy in self.map.cur_room.enemies:
            if self.player:
                if self.player.sprite.hitbox.colliderect(enemy.sprite.hitbox):
                    self.player.damage(enemy.attack)
                    enemy.damage(self.player.attack)
                    
                if self.player.sword.rect and self.player.sword.rect.colliderect(enemy.sprite.hitbox):
                    print("Sword collided with the enemy")
                    enemy.damage(self.player.sword.attack)
                    #print(f"enemy iFrames:{enemy.iFrame_timer}")
                    print("Enemy health: ", enemy.health)
                    #print(f"Player attack timer: {self.player.attack_timer}")
            #print(f"enemy: {enemy.health}")

    def item_collisions(self):
        # Check for item collisions
        for item in self.map.cur_room.items:
            if self.player:
                if self.player.sprite.hitbox.colliderect(item.sprite.hitbox):
                    print("collided with item")
                    if isinstance(item, Key):
                        self.player.keys += 1
                        self.map.cur_room.items.remove(item)
                    elif isinstance(item, Gold):
                        self.player.gold += 1
                        self.map.cur_room.items.remove(item)
                    elif isinstance(item, Heart):
                        healed = self.player.heal(item.heal_amt)
                        if healed: # only remove the heart if it actually healed 
                            self.map.cur_room.items.remove(item)
                    elif isinstance(item, Chest):
                        self.wall_behavior(item, self.player, item.i, item.j)
    
    def item_actions(self):
        for item in self.map.cur_room.items:
            if self.player:
                if isinstance(item, Chest):
                    contained_item = item.open(self.player) # tries to open the chest if conditions are correct
                    if contained_item:
                        self.map.cur_room.add_item(contained_item)

    def tile_collisions(self):
         # Check for tilemap collisions like walls, pits, doors etc.
        for i in range(len(self.tilemap.cur_room_tiles)):
            for j in range(len(self.tilemap.cur_room_tiles[0])):
                tile = self.tilemap.cur_room_tiles[i][j]
                self.wall_collisions(tile, i, j)
                self.door_collisions(tile, i, j)
                self.pit_collisions(tile, i, j)

    def collision_check(self):
        self.player_enemy_collisions()
        self.item_collisions()
        self.tile_collisions()

    # tile can be a tile or an item
    def wall_behavior(self, tile, colliding_entity, i, j):
        colliding_entity_center = colliding_entity.sprite.hitbox.center

        if isinstance(tile, Tile):
            wall_center = tile.get_rect(j,i).center
        elif isinstance(tile, Item):
            wall_center = tile.sprite.get_sprite_center()
        
        if not wall_center:
            print("Wall center is null")
        colliding_entity.wall_bounce(colliding_entity_center, wall_center)
    
    def wall_collisions(self, tile, i, j):
        if type(tile) == Wall or type(tile) == Pillar:
            if self.player and self.player.sprite.hitbox.colliderect(tile.get_rect(j,i)):
                self.wall_behavior(tile, self.player, i, j)

            for enemy in self.map.cur_room.enemies:
                if enemy and enemy.sprite.hitbox.colliderect(tile.get_rect(j,i)):
                    self.wall_behavior(tile, enemy, i, j)
                    enemy.move_in_random_dir()

    def pit_collisions(self, tile, i, j):
        if type(tile) == Pit:
            if self.player and self.player.sprite.hitbox.colliderect(tile.get_rect(j,i)):
                #self.wall_behavior(tile, self.player, i, j)
                self.player.damage(1)
                self.player.spawn_at_respawn_room_coord()

            for enemy in self.map.cur_room.enemies:
                if enemy.sprite.hitbox.colliderect(tile.get_rect(j,i)):
                    #self.wall_behavior(tile, enemy, i, j)
                    pass

    def door_collisions(self, tile, i, j):
        if self.player and self.player.sprite.hitbox.colliderect(tile.get_rect(j,i)): # if collided with tile
            if type(tile) == Door or (type(tile) == LockedDoor and not tile.locked):
                door = tile
                if door.direction == Direction.UP:
                    self.map.cur_room = self.map.cur_room.get_north_room()
                    print("Went up a room")
                    self.player.spawn_at_south_door()
                elif door.direction == Direction.DOWN:
                    self.map.cur_room = self.map.cur_room.get_south_room() 
                    self.player.spawn_at_north_door()
                elif door.direction == Direction.LEFT:
                    self.map.cur_room = self.map.cur_room.get_west_room()        
                    self.player.spawn_at_east_door()
                elif door.direction == Direction.RIGHT:
                    self.map.cur_room = self.map.cur_room.get_east_room()
                    self.player.spawn_at_west_door()
                
                # draw the new room
                self.tilemap.set_new_cur_room_tiles(self.map.cur_room.tiles)
            elif type(tile) == LockedDoor and tile.locked:
                locked_door = tile
                print("The door is locked")
                if self.player.has_keys():
                    self.player.keys -= 1
                    self.map.cur_room.unlock_door(locked_door)
                    print("Unlocked the door")
                else:
                    self.wall_behavior(locked_door, self.player, i, j)

    def draw(self):
        screen.fill(self.bg_color)
        self.tilemap.draw()
        
        for enemy in self.map.cur_room.enemies:
            enemy.draw()
        for item in self.map.cur_room.items:
            item.draw()

        if self.player:
            self.player.draw()
        self.ui.draw()

        if self.game_over:
            self.ui.draw_game_over_screen()
        #draw_point(8,8)
        
    def move(self):
        if self.player:
            self.player.move()

        for enemy in self.map.cur_room.enemies:
            enemy.move()
            #print(enemy.moving_dir)
            if isinstance(enemy, Skeleton):
                enemy.patrol()
    
    
