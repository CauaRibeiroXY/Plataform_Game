import pgzrun
from pygame import Rect
WIDTH = 800
HEIGHT = 600



game_state = "menu"  # Pode ser "menu", "playing" ou "exit"
music_on = True


menu_options = ["Start Game", "Toggle Music","Exit"]
selected_option = None  # Para saber qual o jogador clicou

#musica
music_playing = False

#camera
camera_x = 0
camera_y = 0

def draw():
    screen.clear()

    if game_state == "menu":
        draw_menu()
    elif game_state == "playing":
        screen.draw.text("Game Started!", center=(WIDTH/2, HEIGHT/2), fontsize=50, color="white")
        screen.clear()
        for back in background:
            back.draw()
        player.draw()
        hud.draw()
        for enemy in enemies:
            if enemy.live:
                enemy.draw()
        
        for plat in platforms:
            plat.draw()
    elif game_state == "end_game":
        screen.fill((0,0,0))
        screen.draw.text("End Game",center=(WIDTH/2, HEIGHT/2), fontsize=50, color="white")



def draw_menu():
    global music_playing

    screen.draw.text("MAIN MENU", center=(WIDTH/2, 100), fontsize=60, color="yellow")

    for i, option in enumerate(menu_options):
        screen.draw.text(
            option,
            center=(WIDTH/2, 200 + i * 80),
            fontsize=40,
            color="white"
        )


def on_mouse_down(pos):
    global game_state, music_on

    if game_state == "menu":
        for i, option in enumerate(menu_options):
            x, y = WIDTH/2, 200 + i * 80
            if abs(pos[0] - x) < 150 and abs(pos[1] - y) < 40:
                if option == "Start Game":
                    start_game()
                    game_state = "playing"
                elif option == "Toggle Music":
                    music_on = not music_on
                    if music_on:
                          music.play("tema")
                          music.set_volume(0.5)
                    else:
                        music.stop()
                elif option == "Exit":
                    exit()

class Background:
    def __init__(self,x=0,y=0,water=False):
        self.x = x
        self.y = y

        self.water = water
            
        self.background_sky = Actor("background/background_clouds.png")
        self.background_floor = Actor("background/background_solid_dirt.png")
        self.background_sky_solid = Actor("background/background_solid_sky.png")
        self.background_water_moving = Actor("background/background_water.png")

        

        #Dimension
        self.width = 256
        self.height = 256
        self.background_sky.pos = 0,0
        self.background_floor.pos=100,500
        self.background_sky_solid.pos = 0,0

        if self.water == True:
            self.width = 128
            self.height = 128

    def draw(self):
        if self.water == True:
            self.background_water_moving.topleft = (self.x - camera_x, self.y)
            self.background_water_moving.draw()
            return
            
        
        for i in range(0,WIDTH,self.width):
                self.background_sky.topleft = i,0
                self.background_sky.draw()
        for i in range(0,WIDTH,self.width):
                self.background_sky_solid.topleft = i,256
                self.background_sky_solid.draw()
        for i in range(0,WIDTH,self.width):
                self.background_floor.topleft = i,500
                self.background_floor.draw()
        
            


class Player:
    def __init__(self,enemies_list):
        # Position
        self.x = 100
        self.y = 400

        # Player dimension
        self.width = 80
        self.height = 110

        # Velocity
        self.vx = 0
        self.vy = 0

        # State
        self.on_ground = False
        self.facing_right = True
        self.invulnerable = False
        self.invulnerable_timer = 0

        #Life
        self.lives = 3



        # Sprites
        self.sprites_idle_right = [Actor("player/player_idle.png"),Actor("player/player_stand.png")]
        self.sprites_idle_left = [Actor("player/player_left_idle.png"),Actor("player/player_stand_left.png")]
        self.sprites_walk_right = [Actor("player/player_walk1.png"), Actor("player/player_walk2.png")]
        self.sprites_walk_left = [Actor("player/player_left_walk1.png"), Actor("player/player_left_walk2.png")]
        self.sprites_jump = [Actor("player/player_jump.png")]

        # Current sprite sequence
        self.current_sprites = self.sprites_idle_right
        self.current_sprite = self.current_sprites[0]
        self.sprite_index = 0
        self.frame_count = 0

    def get_live(self):
        return self.lives

    def check_colision(self,enemy):
        
        # Collision with platforms
        self.on_ground = False
        for plat in platforms:
            # Collision Fall
            if self.vy >= 0:
                if (self.y + self.height/2 >= plat.rect.top and
                    self.y + self.height/2 <= plat.rect.top + self.vy and
                    self.x + self.width/2 > plat.rect.left and
                    self.x - self.width/2 < plat.rect.right):
                    self.y = plat.rect.top - self.height/2
                    self.vy = 0
                    self.on_ground = True
        
        #Colison enemy
        if not enemy.live:
            return False
        #hitbox player
        player_left = self.x - self.width/2
        player_right = self.x + self.width/2
        player_top = self.y - self.height/2
        player_bottom = self.y + self.height/2

        #hitbox enemy
        enemy_left = enemy.x - enemy.width/2
        enemy_right = enemy.x + enemy.width/2
        enemy_top = enemy.y - enemy.height/2
        enemy_bottom = enemy.y + enemy.height/2

        #Interseciton
        overlap_bottom = player_bottom - enemy_top
        overlap_top = enemy_bottom - player_top

        if (player_right > enemy_left and
            player_left < enemy_right and
            player_bottom > enemy_top and
            player_top < enemy_bottom):
            if (self.vy > 0 and overlap_bottom < self.height/2):
                self.vy = -10
                sounds.sfx_disappear.play()
                enemy.live = False #Kill enemy
            elif (player_right > enemy_left or player_right < enemy_left) and (player_left < enemy_right or player_left > enemy_right):
                if not self.invulnerable:
                    if self.vx > 0:
                        self.vx = -8
                    else:
                        self.vx = 8
                    sounds.sfx_hurt.play()
                    self.lives -= 0.5
                    self.invulnerable = True
                    self.invulnerable_timer = 120
            
        if self.y > 600:
            print(player_bottom)
            self.lives -= 0.5
            self.x = 100
            self.y = 400
                

    def move_left(self):
        self.vx = -5
        self.facing_right = False

    def move_right(self):
        self.vx = 5
        self.facing_right = True

    def stop(self):
        self.vx = 0

    def jump(self):
        if self.on_ground:
            self.vy = -15
            self.on_ground = False
            sounds.sfx_jump.play()
    

    def update(self, platforms, enemies_list):

        gravity = 0.5
        self.vy += gravity
        self.y += self.vy
        self.x += self.vx

        # Movement input
        if keyboard.left:
            self.move_left()
        elif keyboard.right:
            self.move_right()
        else:
            self.stop()

        if keyboard.space or keyboard.up:
            self.jump()
        
        if self.invulnerable:
            self.invulnerable_timer -=1
            if self.invulnerable_timer <= 0:
                self.invulnerable = False
        

        # Animation selection
        if self.vx > 0:
            self.current_sprites = self.sprites_walk_right
            self.facing_right = True
        elif self.vx < 0:
            self.current_sprites = self.sprites_walk_left
            self.facing_right = False
        else:
            if self.facing_right:
                self.current_sprites = self.sprites_idle_right
            else:
                self.current_sprites = self.sprites_idle_left

        # Animation update
        self.frame_count += 1
        if self.current_sprites == self.sprites_idle_right or self.current_sprites == self.sprites_idle_left :
            if self.frame_count % 20 == 0:
                self.sprite_index = (self.sprite_index + 1) % len(self.current_sprites)
                self.current_sprite = self.current_sprites[self.sprite_index]
        else:
            if self.frame_count % 10 == 0:
                self.sprite_index = (self.sprite_index + 1) % len(self.current_sprites)
                self.current_sprite = self.current_sprites[self.sprite_index]

        for enemy in enemies_list[:]:
            if self.check_colision(enemy):
                enemies_list.remove(enemy)
    
    def draw(self):
        self.current_sprite.pos = (self.x - camera_x, self.y)
        self.current_sprite.draw()

            
class Platform:
    def __init__(self, x, y, num_blocks, direction="horizontal",final = False):
        self.x = x
        self.y = y
        self.final = final
        self.num_blocks = num_blocks
        self.direction = direction
        self.block_size = 64
        self.block_image = "level/bricks_grey.png"
        self.sign_exit = "level/sign_exit.png"

        self.sign = Actor(self.sign_exit)

        # Define o Rect para colisões
        if self.direction == "horizontal":
            self.rect = Rect(x, y, self.num_blocks * self.block_size, self.block_size)
        else:  # vertical
            self.rect = Rect(x, y, self.block_size, self.num_blocks * self.block_size)

    def draw(self):
        if self.final:
            self.sign.pos = (self.rect.x - camera_x, self.rect.y)
            self.sign.draw()
            return
        for i in range(self.num_blocks):
            block = Actor(self.block_image)
            if self.direction == "horizontal":
                block.topleft = (self.rect.x + i * self.block_size - camera_x, self.rect.y)
            elif self.direction == "vertical":
                block.topleft = (self.rect.x - camera_x, self.rect.y + i * self.block_size)
            block.draw()

class Enemy_frog:
    def __init__(self, x, y, min_x, max_x):
        # Position
        self.x = x
        self.y = y

        # Dimensions
        self.width = 64
        self.height = 64

        # Velocity
        self.vx = 1  # velocidade inicial
        self.vy = -5


        # State
        self.on_ground = True
        self.facing_right = True
        self.live = True
        self.jump_cooldown = 0 

        # Movement limits
        self.min_x = min_x
        self.max_x = max_x

        # Sprites 
        self.sprites_idle_right = Actor("enemy/frog/frog_idle_right.png")
        self.sprites_idle_left = Actor("enemy/frog/frog_idle.png")
        self.sprites_jump_right = Actor("enemy/frog/frog_jump_right.png")
        self.sprites_jump_left = Actor("enemy/frog/frog_jump.png")
        self.sprites_rest_right = Actor("enemy/frog/frog_rest_right.png")
        self.sprites_rest_left = Actor("enemy/frog/frog_rest.png")

        # Current sprite sequence
        self.current_sprite = self.sprites_idle_right

    def jump(self):
        self.vy = -10
        if self.facing_right:
            self.vx = 2
        else:
            self.vx = -2
        
    def update(self):
        if not self.live:
            
            return
        
        
        # Gravity
        self.gravity = 0.5
        self.vy += self.gravity
        self.x += self.vx
        self.y += self.vy

        #Colision
        self.on_ground = False
        for plat in platforms:
           if self.vy >= 0:
                if (self.y + self.height/2 >= plat.rect.top and
                    self.y + self.height/2 <= plat.rect.top + self.vy and
                    self.x + self.width/2 > plat.rect.left and
                    self.x - self.width/2 < plat.rect.right):
                    self.y = plat.rect.top - self.height/2
                    self.vy = 0
                    self.on_ground = True
                    if self.jump_cooldown <= 0:
                        self.jump()
                        self.jump_cooldown = 90

        # Change direction
        if self.x < self.min_x:
            self.x = self.min_x
            self.facing_right = True
            if self.on_ground:
                self.jump()
        elif self.x > self.max_x:
            self.x = self.max_x
            self.facing_right = False
            if self.on_ground:
                self.jump()
        
        if self.jump_cooldown > 0:
            self.jump_cooldown -= 1

        # Seleção de sprite
        if self.vx > 0:
            self.current_sprite = self.sprites_idle_right
            if self.vy < 0:
                self.current_sprite = self.sprites_jump_right
        elif self.vx < 0:
            self.current_sprite = self.sprites_idle_left
            if self.vy < 0:
                self.current_sprite = self.sprites_jump_left
        else:
            if self.facing_right:
                self.current_sprite = self.sprites_rest_right
            else:
                self.current_sprite = self.sprites_rest_left

 
    def draw(self):
        # Desenho considerando a câmera
        if self.live:
            self.current_sprite.pos = (self.x - camera_x, self.y)
            self.current_sprite.draw()

class Enemy_bee:
    def __init__(self, x, y, min_x, max_x):
        # Position
        self.x = x
        self.y = y

        # Dimensions
        self.width = 64
        self.height = 64

        # Velocity
        self.vx = 5  # velocidade inicial
        self.vy = 0


        # State
        self.on_ground = True
        self.facing_right = True
        self.live = True

        # Movement limits
        self.min_x = min_x
        self.max_x = max_x

        # Sprites 
        self.sprites_idle_right = Actor("enemy/bee/bee_rest.png")
        self.sprites_idle_left = Actor("enemy/bee/bee_rest_left.png")
        self.sprites_a_right = Actor("enemy/bee/bee_a.png")
        self.sprites_a_left = Actor("enemy/bee/bee_a_left.png")
        self.sprites_b_right = Actor("enemy/bee/bee_b.png")
        self.sprites_b_left = Actor("enemy/bee/bee_b_left.png")

        # Current sprite sequence
        self.frame_count = 0
        self.sprite_index = 0
        self.sprites_fly_right = [self.sprites_a_right, self.sprites_b_right]
        self.sprites_fly_left = [self.sprites_a_left, self.sprites_b_left]
        self.current_sprite_vector = self.sprites_fly_right
        self.current_sprite = self.current_sprite_vector[0]
    


    def update(self):
        if not self.live:
            return
        self.x += self.vx
        self.y += self.vy
        
        # Change direction
        if self.x < self.min_x or self.x > self.max_x:
            self.vx *= -1
            self.facing_right = not self.facing_right
        
        # Select sprites
        if self.vx > 0:
            self.current_sprite_vector = self.sprites_fly_right
        elif self.vx < 0:
            self.current_sprite_vector = self.sprites_fly_left

        self.frame_count += 1
        if self.frame_count % 10 == 0:
            self.sprite_index = (self.sprite_index + 1) % len(self.current_sprite_vector)
            self.current_sprite = self.current_sprite_vector[self.sprite_index]
        

 
    def draw(self):
        if self.live:
            self.current_sprite.pos = (self.x - camera_x, self.y)
            self.current_sprite.draw()

class Enemy_fish:
    def __init__(self, x, y, min_y, max_y):
        # Position
        self.x = x
        self.y = y

        # Dimensions
        self.width = 64
        self.height = 64

        #Moviment Start
        self.vx = 0
        self.vy = 3

        # State
        self.on_ground = True
        self.facing_up = True
        self.live = True

        # Movement limits
        self.min_y = min_y
        self.max_y = max_y

        self.fish_idle_up = Actor("enemy/fish/fish_up_rest.png")
        self.fish_idle_down = Actor("enemy/fish/fish_down_rest.png")
        self.fish_up = Actor("enemy/fish/fish_up.png")
        self.fish_up2 = Actor("enemy/fish/fish_up2.png")
        self.fish_down = Actor("enemy/fish/fish_down.png")
        
        self.frame_count = 0
        self.sprite_index = 0

        self.fish_jump = [self.fish_up,self.fish_up2]
        self.fish_fall = [self.fish_down,self.fish_idle_down]
        self.current_sprite_vector = self.fish_jump
        self.current_sprite = self.current_sprite_vector[0]
        

    def update(self):
        if not self.live:
            return

        self.y += self.vy

        
        # Change direction
        if self.y > self.min_y or self.y < self.max_y:
            self.vy *= -1
            self.facing_up = not self.facing_up
        
        # Select sprites
        if self.vy > 0:
            self.current_sprite_vector = self.fish_fall
        elif self.vy < 0:
            self.current_sprite_vector = self.fish_jump

        self.frame_count += 1
        if self.frame_count % 10 == 0:
            self.sprite_index = (self.sprite_index + 1) % len(self.current_sprite_vector)
            self.current_sprite = self.current_sprite_vector[self.sprite_index]


    def draw(self):    
        if self.live:
            self.current_sprite.pos = (self.x - camera_x, self.y)
            self.current_sprite.draw()



class Hud_life:
    def __init__(self, Player):
        #position
        self.x = 32
        self.y = 32

        # Dimensions
        self.width = 64
        self.height = 64

        

    def update(self,Player):
        self.lives = Player.get_live()
        #Sprites
        self.life_full = Actor("player/hud_heart.png")
        self.life_half = Actor("player/hud_heart_half.png")
        self.life_empty = Actor("player/hud_heart_empty.png")

        self.current = self.life_full
        self.current.sprite_vector=[]
        self.current.sprite_vector.append(self.life_full) 
        self.current.sprite_vector.append(self.life_full) 
        self.current.sprite_vector.append(self.life_full) 
        
        
        for i in range(3):
            if self.lives >= i + 1:
                self.current.sprite_vector[i] = self.life_full
            elif self.lives > i:
                self.current.sprite_vector[i] = self.life_half
            else:
                self.current.sprite_vector[i] = self.life_empty

    def draw(self):
        for i in range(3):
            self.current.sprite = self.current.sprite_vector[i]
            self.current.sprite.pos = (self.x + i * self.width, self.y)
            self.current.sprite.draw()



def update():
    global camera_x, camera_y,game_state,music_playing
    if music_on and not music_playing:
        music.play("tema")
        music.set_volume(0.5)
        music_playing = True
    elif not music_on and music_playing:
        music.stop()
        music_playing = False

    if game_state == "playing" and player:
        
        for enemy in enemies:
            enemy.update()
        player.update(platforms,enemies)
        hud.update(player)
        camera_x = player.x - WIDTH/2
        for plat in platforms:
            if plat.final:
                # Checa colisão simples (ajuste se necessário)
                if (player.x + player.width/2 > plat.rect.left and
                    player.x - player.width/2 < plat.rect.right and
                    player.y + player.height/2 > plat.rect.top and
                    player.y - player.height/2 < plat.rect.bottom):
                    # 3. Muda o estado do jogo
                    game_state = "end_game"



def start_game():
    global platforms, player, enemies,hud,background
    background = [Background(),Background(1780,500,True),Background(1908,500,True),Background(1908+128,500,True)]
    platforms = [
    Platform(0, 500, 5, "horizontal"),
    Platform(300, 350, 3, "horizontal"),
    Platform(500, 500, 20, "horizontal"),
    Platform(1908+128+64, 350, 20, "horizontal"),
    Platform(3350, 320, 1, "horizontal",True)

    ]
    
    enemies = []
    plat = platforms[2]

    enemies.append(Enemy_frog(564,plat.y - 32,564,700))
    enemies.append(Enemy_frog(700,plat.y - 32,700,1000))
    enemies.append(Enemy_bee(100,200,100,500))
    enemies.append(Enemy_bee(500,200,500,900))
    enemies.append(Enemy_fish(1840,400,600,300))
    enemies.append(Enemy_fish(1908+128,400,600,300))


    player = Player(enemies)
    hud = Hud_life(player)










start_game()
pgzrun.go()
