import pygame,sys,random,pickle
pygame.init()

# set up
WIDTH,HEIGHT = 704,590
win = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Platform Soldier")

# functions
def loadImg(path):
    return pygame.image.load('Assets/'+path+'.png').convert_alpha()
def scale(name,size1,size2):
    return pygame.transform.scale(name,(size1,size2))
def flip(name):
    return pygame.transform.flip(name,True,False)
def text(msg,x,y,color,font,size):
    style = pygame.font.SysFont(font,size)
    textmsg = style.render(msg,1,color)
    return win.blit(textmsg,(x,y))

# game variable
'''
-1 - empty
0 - ground
1 - soil
2 - water surface
3 - deep water
4 - small rock
5 - big rock
6 - box
7 - grass
8 - exit
9 - ammo
10 - health
11 - grenade
12 - enemy
'''
ROW = 129
COLS = 15
TILE_SIZE = 32
img1 = loadImg('Tiles/0')
img2 = loadImg('Tiles/1')
img3 = loadImg('Tiles/2')
img4 = loadImg('Tiles/3')
img5 = loadImg('Tiles/4')
img6 = loadImg('Tiles/5')
img7 = loadImg('Tiles/6')
img8 = loadImg('Tiles/7')
img9 = loadImg('Tiles/8')
bg1 = loadImg('Background/sky_cloud')
bg2 = loadImg('Background/mountain')
bg3 = loadImg('Background/pine1')
bg4 = loadImg('Background/pine2')
bullet_img = loadImg('Player/bullet')
grenade_img = loadImg('Player/grenade')
jump_audio = pygame.mixer.Sound('Assets/Audio/audio_jump.wav')
shot_audio = pygame.mixer.Sound('Assets/Audio/audio_shot.wav')
grenade_audio = pygame.mixer.Sound('Assets/Audio/audio_grenade.wav')
MAX_LEVEL = 3

def Map():
    world_data = []
    for row in range(ROW):
        r  = [-1]*COLS
        world_data.append(r)

    world_data = []
    pickle_in = open(f'level{level}', 'rb')
    world_data = pickle.load(pickle_in)

    tile_rects = []
    tile_list = []
    water_list = []
    exit_list = []
    for y, row in enumerate(world_data):
        for x, tile in enumerate(row):
            if tile == 0:     # ground
                img = img1
                img_rect = img.get_rect()
                img_rect.x = x*TILE_SIZE
                img_rect.y = (y*TILE_SIZE)+110
                tile_data = (img,img_rect)
                tile_list.append(tile_data)
            if tile == 1:     # soil
                img = img2
                img_rect = img.get_rect()
                img_rect.x = x*TILE_SIZE
                img_rect.y = (y*TILE_SIZE)+110
                tile_data = (img,img_rect)
                tile_list.append(tile_data)
            if tile == 2:     # water surface
                img = img3
                img_rect = img.get_rect()
                img_rect.x = x*TILE_SIZE
                img_rect.y = (y*TILE_SIZE)+110
                tile_data = (img,img_rect)
                tile_list.append(tile_data)
                water_list.append(img_rect)
            if tile == 3:     # deep water
                img = img4
                img_rect = img.get_rect()
                img_rect.x = x*TILE_SIZE
                img_rect.y = (y*TILE_SIZE)+110
                tile_data = (img,img_rect)
                tile_list.append(tile_data)
                water_list.append(img_rect)
            if tile == 4:     # small rocks
                img = img5
                img_rect = img.get_rect()
                img_rect.x = x*TILE_SIZE
                img_rect.y = (y*TILE_SIZE)+110
                tile_data = (img,img_rect)
                tile_list.append(tile_data)
            if tile == 5:     # big rocks
                img = img6
                img_rect = img.get_rect()
                img_rect.x = x*TILE_SIZE
                img_rect.y = (y*TILE_SIZE)+110
                tile_data = (img,img_rect)
                tile_list.append(tile_data)
            if tile == 6:     # box
                img = img7
                img_rect = img.get_rect()
                img_rect.x = x*TILE_SIZE
                img_rect.y = (y*TILE_SIZE)+110
                tile_data = (img,img_rect)
                tile_list.append(tile_data)
            if tile == 7:     # grass
                img = img8
                img_rect = img.get_rect()
                img_rect.x = x*TILE_SIZE
                img_rect.y = (y*TILE_SIZE)+110
                tile_data = (img,img_rect)
                tile_list.append(tile_data)
            if tile == 8:     # exit
                img = img9
                img_rect = img.get_rect()
                img_rect.x = x*TILE_SIZE
                img_rect.y = (y*TILE_SIZE)+110
                tile_data = (img,img_rect)
                tile_list.append(tile_data)
                exit_list.append(img_rect)
            if tile == 11:
                grenade = ItemBox('grenade',x*TILE_SIZE,(y*TILE_SIZE)+110)
                item_box.add(grenade)
            if tile == 10:
                medic = ItemBox('medic',x*TILE_SIZE,(y*TILE_SIZE)+110)
                item_box.add(medic)
            if tile == 9:
                ammo = ItemBox('ammo',x*TILE_SIZE,(y*TILE_SIZE)+110)
                item_box.add(ammo)
            if tile == 12:
                enemy = Player('Enemy',x*TILE_SIZE,(y*TILE_SIZE)+110)
                enemy_group.add(enemy)
            if tile!=-1 and tile!=2 and tile!=3 and tile!=4 and tile!=5 and tile!=7 and tile!=11 and tile!=12 and tile!=9 and tile!=10 and tile!=8:
                tile_rect = pygame.Rect(x*TILE_SIZE,(y*TILE_SIZE)+110,TILE_SIZE,TILE_SIZE)
                tile_rects.append(tile_rect)

    return tile_rects,tile_list,water_list,exit_list

def drawMap():
    for tile in tile_data[1]:
        tile[1][0] += player.sprite.scroll
        win.blit(tile[0],tile[1])
    for tile in tile_data[0]:
        tile.x += player.sprite.scroll

class Exit(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = img9
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        if self.rect.colliderect(player.sprite.rect):
            win.fill((0,0,0))

class Player(pygame.sprite.Sprite):
    def __init__(self,char_type,x,y):
        super().__init__()
        self.char_type = char_type
        self.vel = 7
        self.index = 0
        self.gravity = 0
        self.animation_list = []
        self.run_list = []
        self.death_list = []
        self.img_w = 45
        self.img_h = 65
        for i in range(5):
            img = loadImg(f'{self.char_type}/Idle/{i}')
            img = scale(img,self.img_w,self.img_h)
            self.animation_list.append(img)
        for i in range(6):
            img = loadImg(f'{self.char_type}/Run/{i}')
            img = scale(img,self.img_w,self.img_h)
            self.run_list.append(img)
        for i in range(8):
            img = loadImg(f'{self.char_type}/Death/{i}')
            img = scale(img,self.img_w+10,self.img_h)
            self.death_list.append(img)
        self.image = self.animation_list[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.left = False
        self.right = False
        self.idle = True
        self.dir = 1
        self.health = 100
        self.alive = True
        self.jump_img =  scale(loadImg(f'{self.char_type}/Jump'),self.img_w,self.img_h)
        self.move_counter = 0
        self.supervise_distance = 10
        self.in_air = False
        self.scroll = 0
        self.map_distance = 0
        self.game_over = False

    def healthBar(self):
        if self.char_type == 'Enemy':
            if self.alive:    #alive
                health_bar_border = pygame.Rect(self.rect.x - 15,self.rect.y - 15,70,11)        #health bar
                pygame.draw.rect(win,(200,20,20),health_bar_border,2)
                if self.health <= 100:
                    health_bar_width = self.health*(66/100)
                if self.health > 100:
                    health_bar_width = 66
                health_bar = pygame.Rect(self.rect.x - 13, self.rect.y - 13,health_bar_width,7)
                pygame.draw.rect(win,(10,200,10),health_bar)

    def actions(self):
        if self.idle:
            self.index += 0.4
            if self.index >= len(self.animation_list):
                self.index = 0
            if self.dir == 1:
                self.image = self.animation_list[int(self.index)]
            elif self.dir == -1:
                self.image = flip(self.animation_list[int(self.index)])

        if self.right:
            self.dir = 1
            if self.char_type == 'Player':
                self.index += 0.6
            elif self.char_type == 'Enemy':
                self.index += 0.1
            if self.index >= len(self.run_list):
                self.index = 0
            self.image = self.run_list[int(self.index)]

        if self.left:
            self.dir = -1
            if self.char_type == 'Player':
                self.index += 0.6
            elif self.char_type == 'Enemy':
                self.index += 0.1
            if self.index >= len(self.run_list):
                self.index = 0
            self.image = flip(self.run_list[int(self.index)])

    def handlingPlayer(self):
        dx = 0
        dy = 0

        key = pygame.key.get_pressed()

        if self.char_type == 'Player':

            if self.alive:    # player alive

                if player.sprite.health < 0:    #check health
                        player.sprite.health = 0
                if player.sprite.health <= 0:
                        self.alive = False
                
                self.idle = True    #idle

                if key[pygame.K_RIGHT] and self.rect.right <= WIDTH and player.sprite.alive:    #right
                    dx += self.vel
                    self.right = True
                    self.left = False
                    self.idle = False
                else:
                    self.right = False

                if key[pygame.K_LEFT] and self.rect.left > 0 and player.sprite.alive:   #left
                    dx -= self.vel
                    self.left = True
                    self.right = False
                    self.idle = False
                else:
                    self.left = False

                if key[pygame.K_SPACE] and self.in_air == False:      #jump
                    jump_audio.play()
                    self.gravity = -40
                    if self.left:
                        self.image = flip(self.jump_img)
                    if self.right:
                        self.image = self.jump_img
                    self.in_air = True

            else:                       # player not alive
                self.idle = False
                self.right = False
                self.left = False
                self.index += 0.5
                if self.index >= len(self.death_list):
                    self.index = len(self.death_list)-1
                    self.game_over = True
                if self.dir == -1:
                    player.sprite.image = flip(self.death_list[int(self.index)])
                else:
                    player.sprite.image = self.death_list[int(self.index)]

            self.gravity += 5   #gravity
            dy += self.gravity
            if self.rect.bottom >= HEIGHT:
                self.rect.bottom = HEIGHT
                self.gravity = 0
                self.rect.y += 0

            for tile in tile_data[0]:     #tile collisions
                if tile.colliderect(self.rect.x+dx,self.rect.y,self.img_w,self.img_h):
                    dx = 0
                if tile.colliderect(self.rect.x,self.rect.y+dy,self.img_w,self.img_h):
                    if self.gravity < 0:    #jumping
                        self.gravity = 0
                        dy =  tile.bottom - self.rect.top 

                    elif self.gravity >= 0:     #falling
                        self.gravity = 0
                        dy = tile.top - self.rect.bottom
                        self.in_air = False

            if self.dir == 1 and self.right == True and self.rect.x > WIDTH-400 and self.map_distance < 93:     #scroll
                self.rect.x += 0
                dx = 0
                self.scroll = -self.vel
                self.map_distance += 1
            elif self.dir == -1 and self.left == True and self.rect.x < 400 and self.map_distance>0:
                self.rect.x += 0
                dx = 0
                self.scroll = self.vel
                self.map_distance -= 1
            else:
                self.scroll = 0

            self.rect.x += dx   #update x movements
            self.rect.y += dy   #update y movements 

    def handlingEnemy(self):
        dx = 0
        dy = 0

        if self.char_type == 'Enemy':

            self.vel = 5

            if self.alive:      #enemy alive

                enemy_shoot = [0,0,0,0,1]

                if self.health < 0:     #check health
                    self.health = 0
                if self.health <= 0:
                    self.alive = False

                if self.dir == 1:
                    self.right = True
                else:
                    self.left = True

                if self.right:         # right
                    dx += self.vel
                    self.move_counter += 0.8
                    if self.move_counter > self.supervise_distance:
                        self.right = False
                        self.left = True
                        self.move_counter = 0
                        self.dir *= -1
                    enemy_vision = pygame.Rect(self.rect.right-30,self.rect.y+10,150,self.rect.height-20)
                    bullet_x = self.rect.right+10
                    for tile in tile_data[0]:     #tile collisions
                        if tile.colliderect(self.rect.x+dx,self.rect.y,self.img_w,self.img_h):
                            dx = 0
                            self.rect.x += 0
                            self.move_counter = 0
                            self.right = False
                            self.left = True
                            self.dir *= -1
                    
                if self.left:          # left
                    dx -= self.vel
                    self.move_counter += 0.8
                    if self.move_counter > self.supervise_distance:
                        self.right = True
                        self.left = False
                        self.move_counter = 0
                        self.dir *= -1
                    enemy_vision = pygame.Rect(self.rect.x-120,self.rect.y+10,150,self.rect.height-20)
                    bullet_x = self.rect.left-10
                    for tile in tile_data[0]:     #tile collisions
                        if tile.colliderect(self.rect.x+dx,self.rect.y,self.img_w,self.img_h):
                            dx = 0
                            self.rect.x += 0
                            self.move_counter = 0
                            self.right = True
                            self.left = False
                            self.dir *= -1

                if enemy_vision.colliderect(player.sprite.rect) and player.sprite.alive:
                    shoot = random.choice(enemy_shoot)
                    self.idle = True
                    self.right = False
                    self.left = False
                    self.move_counter = 0
                    if shoot == 1 and player.sprite.alive:
                        shot_audio.play()
                        bullet.add(Bullet(bullet_x,self.rect.y+(self.img_h/2)+2,self.dir,'Enemy'))
                    dx = 0
                    self.rect.x += 0
                else:
                    if self.dir == 1:
                        self.right = True
                        self.left = False
                    else:
                        self.left = True
                        self.right = False

            else:
                self.index += 0.5
                if self.index >= len(self.death_list):
                        self.index = len(self.death_list)-1
                if self.dir == -1:
                    self.image = flip(self.death_list[int(self.index)])
                else:
                    self.image = self.death_list[int(self.index)]
                self.idle = False
                self.right = False
                self.left = False
                self.move_counter = 0

            self.rect.x += player.sprite.scroll
            
            self.gravity += 3   #gravity
            dy += self.gravity
            if self.rect.bottom >= HEIGHT:
                self.rect.bottom = HEIGHT
                self.gravity = 0
                self.rect.y += 0

            for tile in tile_data[0]:
                if tile.colliderect(self.rect.x,self.rect.y+dy,self.img_w,self.img_h):
                    dy = tile.top - self.rect.bottom
                    if self.gravity >= 0:     #falling
                        self.gravity = 0
                        self.rect.y += 0

            self.rect.x += dx
            self.rect.y += dy

    def panelBox(self):
        global num_ammo,num_grenade
        text('Health: ',10,15,(0,0,0),'comicsans',30)           #health bar
        health_bar_border = pygame.Rect(100,10,200,30)        
        pygame.draw.rect(win,(0,0,0),health_bar_border,2)
        if player.sprite.health <= 100:
            health_bar_width = player.sprite.health*(197/100)
        if player.sprite.health > 100:
            player.sprite.health = 100
            health_bar_width = 197
        health_bar = pygame.Rect(102, 12,health_bar_width,27)
        health_color = (10,200,10)
        if health_bar_width <= 95 and health_bar_width >= 40:
            health_color = (200,200,10)
        elif health_bar_width < 40:
            health_color = (200,10,10)
        pygame.draw.rect(win,health_color,health_bar)
        if num_ammo > 40:
            num_ammo = 40
        text('Ammo: ',10,55,(0,0,0),'comicsans',30)             #ammo
        for i in range (num_ammo):
            win.blit(bullet_img,(100+(i*20),60))
        if num_grenade > 38:
            num_grenade = 38
        text('Grenade: ',10,90,(0,0,0),'comicsans',30)          #grenade
        for i in range (num_grenade):
            win.blit(grenade_img,(120+(i*20),95))

    def update(self):
        if not_move == False:
            self.handlingPlayer()
            self.handlingEnemy()
            self.panelBox()
            self.actions()

    def draw(self):
        win.blit(self.image, self.rect)

class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y,direction,char_type):
        super().__init__()
        self.image = bullet_img
        self.rect = self.image.get_rect(center = (x,y))
        self.vel = 7
        self.char_type = char_type
        self.mask = pygame.mask.from_surface(self.image)
        self.bullet_list = []
        self.direction = direction
        if self.direction == -1:
            if self.char_type == 'Player':
                self.rect.x = player.sprite.rect.x - 10

    def update(self):
        self.rect.x += player.sprite.scroll      #scroll
        self.rect.x += (self.direction*self.vel)    #movement

        if self.rect.x > WIDTH+10 or self.rect.x < -10:     # boundaries
            self.kill()

        for enemy in enemy_group:   # hit enemy
            if enemy.alive:
                if pygame.sprite.spritecollide(enemy,bullet,False,pygame.sprite.collide_mask):
                    self.kill()
                    if self.char_type == 'Player':
                        enemy.health -= 25
                        
        if player.sprite.alive:     #hit player
            if pygame.sprite.spritecollide(player.sprite,bullet,False,pygame.sprite.collide_mask):
                self.kill()
                if self.char_type == 'Enemy':
                    player.sprite.health -= 10

        for tile in tile_data[0]:     # hit tiles
            if tile.colliderect(self.rect):
                self.kill()

class Grenade(pygame.sprite.Sprite):
    def __init__(self,x,y,direction):
        super().__init__()
        self.image = grenade_img
        self.rect = self.image.get_rect(center = (x,y))
        self.vel = 6
        self.dir = 1
        self.mask = pygame.mask.from_surface(self.image)
        self.bullet_list = []
        self.direction = direction
        self.gravity = -20
        if player.sprite.dir == -1:
            self.rect.x = player.sprite.rect.x-5
        self.timer = 100

    def update(self):
        dx = 0 
        dy = 0

        self.rect.x += player.sprite.scroll  #scroll

        self.gravity += 1.5     #gravity
        dy += self.gravity
        dx += (self.direction*self.vel)     # x movement

        if self.rect.x >= WIDTH or self.rect.x <= 0:    # bounce back
            self.direction = self.direction*-1

        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
            self.vel = 0

        self.timer -= 1.7       # explosion
        if self.timer <=0 :
            self.kill()
            grenade_audio.play()
            explosion.add(Explosion(self.rect.x-25,self.rect.y-60))

        for tile in tile_data[0]:
            if tile.colliderect(self.rect.x+dx,self.rect.y,self.rect.width,self.rect.height):   # bounce back
                self.direction = self.direction*-2
                dx += (self.direction*self.vel) 
            if tile.colliderect(self.rect.x,self.rect.y+dy,self.rect.width,self.rect.height):
                self.vel = 0
                if self.gravity < 0:    # hit top tiles
                    self.gravity = 0
                    dy = tile.bottom - self.rect.top
                elif self.gravity > 0:  # hit bottom tiles
                    self.gravity = 0
                    dy = tile.top - self.rect.bottom

        self.rect.x += dx   # update x movement
        self.rect.y += dy   # update y movement

class Explosion(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.img_list = []
        self.index = 0
        for i in range(5):
            img = loadImg(f'Explosions/exp{i+1}')
            self.img_list.append(img)
        self.image = self.img_list[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.x += player.sprite.scroll  #scroll
        self.index += 0.2      # animation
        if self.index < len(self.img_list):
            self.image = self.img_list[int(self.index)]
        else:
            self.kill()     # disappear
        if player.sprite.alive:     # hit player
            if pygame.sprite.spritecollide(player.sprite,explosion,False,pygame.sprite.collide_mask):
                player.sprite.health -= 3
        for enemy in enemy_group:
            if enemy.alive:     # hit enemy
                if pygame.sprite.spritecollide(enemy,explosion,False,pygame.sprite.collide_mask):
                    enemy.health = 0

class ItemBox(pygame.sprite.Sprite):
    def __init__(self,item,x,y):
        super().__init__()
        self.item_type = item
        self.image = scale(loadImg(f'Tiles/item_{self.item_type}'),TILE_SIZE,TILE_SIZE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.gravity = 0

    def update(self):
        global num_ammo,num_grenade

        dy = 0

        self.rect.x += player.sprite.scroll #scroll

        self.gravity += 2   # gravity
        dy += self.gravity
        
        if self.rect.colliderect(player.sprite.rect):
            if self.item_type == 'medic' and player.sprite.health != 100:   #medic
                player.sprite.health += 25
                self.kill()
            if self.item_type == 'ammo' and not num_ammo  >= 40:  #ammo
                num_ammo += 10
                self.kill()
            if self.item_type == 'grenade' and not num_grenade >=38:   #grenade
                num_grenade += 3
                self.kill()

        for tile in tile_data[0]:
            if tile.colliderect(self.rect.x,self.rect.y+dy,self.rect.width,self.rect.height):   #tile collision
                self.gravity = 0
                dy = tile.top - self.rect.bottom

        self.rect.y += dy   # update position

def waterCollision():
    for tile in tile_data[2]:
        if player.sprite.rect.colliderect(tile):
            player.sprite.health = 0

run = True
clock = pygame.time.Clock()
player = pygame.sprite.GroupSingle(Player('Player',10,200))
enemy_group = pygame.sprite.Group()     # enemy group
bullet = pygame.sprite.Group()          # bullet group
grenade = pygame.sprite.Group()         # grenade group
explosion = pygame.sprite.Group()       # explosion group
item_box = pygame.sprite.Group()        # item box group
num_ammo = 7
num_grenade = 2
pygame.time.set_timer(pygame.USEREVENT+1,1000)
counter = 0
level = 0
tile_data = Map()
not_move = False

while run:
    clock.tick(20)

    win.blit(bg1,(0,0))
    win.blit(bg2,(0,100))
    win.blit(bg3,(0,190))
    win.blit(bg4,(0,260))
    drawMap()
    waterCollision()
    for enemies in enemy_group:
        enemies.draw()
        enemies.update()
        enemies.healthBar()
    bullet.draw(win)
    bullet.update()
    grenade.draw(win)
    grenade.update()
    explosion.draw(win)
    explosion.update()
    item_box.draw(win)
    item_box.update()
    player.draw(win)
    player.update()
    if player.sprite.game_over:
        if counter > 1:
            not_move = True
            win.fill((0,0,0))
            text('You lost',260,(HEIGHT/2)-100,(200,200,200),'comic sans',60)
            play_again_btn = pygame.Rect(267,HEIGHT/2,170,45)
            pygame.draw.rect(win,(200,200,200),play_again_btn,border_radius = 20)
            text('Play Again',280,(HEIGHT/2)+10,(0,0,0),'comicsans',20)
            pos = pygame.mouse.get_pos()
            if play_again_btn.collidepoint(pos):
                pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND))
                if pygame.mouse.get_pressed()[0] == 1:
                    player = pygame.sprite.GroupSingle(Player('Player',10,200))
                    enemy_group = pygame.sprite.Group()     # enemy group
                    bullet = pygame.sprite.Group()          # bullet group
                    grenade = pygame.sprite.Group()         # grenade group
                    explosion = pygame.sprite.Group()       # explosion group
                    item_box = pygame.sprite.Group()        # item box group
                    num_ammo = 10
                    num_grenade = 3
                    level += 0
                    tile_data = Map()
                    pygame.time.set_timer(pygame.USEREVENT+1,1000)
                    counter = 0
                    not_move = False
            else:
                pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW))
    for tile in tile_data[3]:
        if player.sprite.rect.colliderect(tile):
            if level < MAX_LEVEL:
                not_move = True
                win.fill((0,0,0))
                text('Level Complete!',210,(HEIGHT/2)-100,(200,200,200),'comic sans',60)
                next_level_btn = pygame.Rect(265,HEIGHT/2,170,45)
                pygame.draw.rect(win,(200,200,200),next_level_btn,border_radius = 20)
                text('Next Level',280,(HEIGHT/2)+10,(0,0,0),'comicsans',20)
                pos = pygame.mouse.get_pos()
                if next_level_btn.collidepoint(pos):
                    pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND))
                    if pygame.mouse.get_pressed()[0] == 1:
                        not_move = False
                        level += 1
                        player = pygame.sprite.GroupSingle(Player('Player',10,200))
                        enemy_group = pygame.sprite.Group()     # enemy group
                        bullet = pygame.sprite.Group()          # bullet group
                        grenade = pygame.sprite.Group()         # grenade group
                        explosion = pygame.sprite.Group()       # explosion group
                        item_box = pygame.sprite.Group()        # item box group
                        num_ammo = 10
                        num_grenade = 3
                        tile_data = Map()
                        pygame.time.set_timer(pygame.USEREVENT+1,1000)
                        counter = 0
                else:
                    pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW))
            else:
                not_move = True
                win.fill((0,0,0))
                text('You won!',260,(HEIGHT/2)-100,(200,200,200),'comic sans',60)
                pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW))

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL and player.sprite.alive and num_ammo > 0:
                shot_audio.play()
                num_ammo -= 1
                bullet.add(Bullet(player.sprite.rect.x+55,player.sprite.rect.y+(player.sprite.img_h/2)+2,player.sprite.dir,'Player'))
            if event.key == pygame.K_RETURN and player.sprite.alive and num_grenade > 0:
                num_grenade -= 1
                grenade.add(Grenade(player.sprite.rect.x+45,player.sprite.rect.y+(player.sprite.img_h/2)+2,player.sprite.dir))

        if event.type == pygame.USEREVENT+1 and player.sprite.game_over == True:
            counter += 1
