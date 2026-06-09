import pygame,sys,random
pygame.init()
# SETUP ---------------------------------------------------
WIDTH,HEIGHT = 700,400
win = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Recycling")
# LOADIMG -------------------------------------------------
def img(name):
    return pygame.image.load(f'Assets\\{name}.png').convert_alpha()
# SCALEIMG -------------------------------------------------
def scale(name,w,h):
    return pygame.transform.scale(name,(w,h))
# FLIPIMG -------------------------------------------------
def flip(name):
    return pygame.transform.flip(name,True,False)
# VARIABLES -----------------------------------------------
player_w = 30
player_h = 50
rightImg = [scale(img('guy1'),player_w,player_h),scale(img('guy2'),player_w,player_h)]
leftImg = [scale(flip(img('guy1')),player_w,player_h),scale(flip(img('guy2')),player_w,player_h)]
bg = img('bg')
bg = scale(bg,WIDTH,HEIGHT)
dirt = img('dirt')
dirt = scale(dirt,50,50)
grass = img('grass')
grass = scale(grass,50,50)
recycling_bin = img('bin')
recycling_bin = scale(recycling_bin,50,50)
score = 0
GAME_OVER_FONT = pygame.font.SysFont('gadugi',40)
PANEL_FONT = pygame.font.SysFont('comicsans',30)
jump_audio = pygame.mixer.Sound('Assets\\jump.mp3')
collect = pygame.mixer.Sound('Assets\\collect.wav')
num_rubbish = 30
num_plastic = 3
over = 'msg'
# TEXT ----------------------------------------------------
def renderText(msg,font,color,x,y):
    text = font.render(msg,1,color)
    return win.blit(text,(x,y))
# LOADMAP ---------------------------------------------
def loadMap():
    game_map = [['0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
                ['0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
                ['0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
                ['0','0','0','0','0','0','0','2','0','0','0','0','0','0'],
                ['0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
                ['0','0','0','0','2','2','0','0','0','0','0','0','2','0'],
                ['2','2','0','0','1','1','0','2','2','2','0','0','1','2'],
                ['1','1','0','0','1','1','0','1','1','1','0','0','1','1']]
    y = 0
    tile_size = 50
    tile_list = []
    for row in game_map:
        x = 0
        for tile in row:
            if tile == '1':
                win.blit(dirt,(x*tile_size,y*tile_size))
            if tile == '2':
                win.blit(grass,(x*tile_size,y*tile_size))
            if tile != '0':
                tile_rect = pygame.Rect(x*tile_size,y*tile_size,tile_size,tile_size)
                tile_list.append(tile_rect)
            x += 1
        y += 1

    return tile_list
# PLAYERCLASS -------------------------------------------
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.leftImg = leftImg
        self.rightImg = rightImg
        self.image = scale(img('guy1'),player_w,player_h)
        self.rect = self.image.get_rect(center = (25,280))
        self.mask = pygame.mask.from_surface(self.image)
        self.index = 0
        self.vel = 3
        self.gravity = 0
        self.hit_list = []
        self.move_right = False
        self.move_left = True

    def animation(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.x > 0:
            self.index += 0.3
            if self.index >= len(self.leftImg):
                self.index = 0
            self.image = self.leftImg[int(self.index)]
            self.rect.x -= self.vel
            self.move_left = True
        elif key[pygame.K_RIGHT] and self.rect.right <= WIDTH:
            self.index += 0.3
            if self.index >= len(self.rightImg):
                self.index = 0
            self.image = self.rightImg[int(self.index)]
            self.rect.x += self.vel
            self.move_right = False

    def jumping(self):
        key = pygame.key.get_pressed()
        self.gravity += 0.4
        self.rect.y += self.gravity
        for tile_rect in returned_list:
            if key[pygame.K_SPACE] and self.rect.bottom >= HEIGHT and self.rect.bottom == tile_rect.top:
                self.gravity = -10
            if key[pygame.K_SPACE] and self.rect.bottom == tile_rect.top:
                jump_audio.play()
                jump_audio.set_volume(0.07)

    def collision(self):
        for tile_rect in returned_list:
            if tile_rect.colliderect(self.rect):
                self.hit_list.append(tile_rect)

        for tile_rect in self.hit_list:
            if tile_rect.colliderect(self.rect):
                if abs(self.rect.right - tile_rect.left) <= 10:
                    self.rect.right = tile_rect.left
                if abs(self.rect.left - tile_rect.right) <= 10:
                    self.rect.left = tile_rect.right
                if abs(self.rect.bottom - tile_rect.top) <= 10:
                    self.gravity = 0
                    key = pygame.key.get_pressed()
                    if key[pygame.K_SPACE]:
                        self.gravity = -10
                    self.rect.bottom = tile_rect.top
                if abs(self.rect.top - tile_rect.bottom) <= 10:
                    self.rect.top = tile_rect.bottom
                    self.gravity += 0.4

    def update(self):
        self.animation()
        self.jumping()
        self.collision()
# RUBBISHCLASS -------------------------------------------
class Rubbish(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.index = 0
        self.img = [scale(img('rubbish1'),40,40),scale(img('rubbish2'),40,40)]
        self.image = self.img [self.index]
        x = random.randint(15,WIDTH-20)
        y = random.randint(60,220)
        self.rect = self.image.get_rect(center = (x,y))
        self.mask = pygame.mask.from_surface(self.image)

    def animation(self):
        self.index += 0.03
        if self.index >= len(self.img):
            self.index = 0
        self.image = self.img[int(self.index)]
    
    def collision(self):
        for tile_rect in returned_list:
            if tile_rect.colliderect(self.rect):
                self.kill()

    def update(self):
        self.animation()
        self.collision()
# PLASTICCLASS -------------------------------------------
class Plastic(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.index = 0
        self.img = [scale(img('plastic1'),40,40),scale(img('plastic2'),40,40)]
        self.image = self.img [self.index]
        x = random.randint(15,WIDTH-100)
        y = random.randint(60,130)
        self.rect = self.image.get_rect(center = (x,y))
        self.mask = pygame.mask.from_surface(self.image)

    def animation(self):
        self.index += 0.03
        if self.index >= len(self.img):
            self.index = 0
        self.image = self.img[int(self.index)]
    
    def collision(self):
        for tile_rect in returned_list:
            if tile_rect.colliderect(self.rect):
                self.kill()

    def update(self):
        self.animation()
        self.collision()
# BIRDCLASS -----------------------------------------------
class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.index = 0
        self.img = [scale(img('bird1'),70,35),scale(img('bird2'),70,35)]
        self.image = self.img [self.index]
        x = WIDTH+50
        y = random.randint(60,230)
        self.rect = self.image.get_rect(center = (x,y))
        self.mask = pygame.mask.from_surface(self.image)
        self.vel = 3

    def animation(self):
        self.index += 0.03
        if self.index >= len(self.img):
            self.index = 0
        self.image = self.img[int(self.index)]
    
    def movement(self):
        self.rect.x -= self.vel
        if self.rect.x < -80:
            self.kill()

    def update(self):
        self.animation()
        self.movement()
# GAMEVARIABLES -------------------------------------------
clock = pygame.time.Clock()
game = True
player = pygame.sprite.GroupSingle(Player())
rubbish_group = pygame.sprite.Group()
for i in range(num_rubbish):
    rubbish_group.add(Rubbish())
plastic_group = pygame.sprite.Group()
for i in range(num_plastic):
    plastic_group.add(Plastic())
bird_group = pygame.sprite.Group()
pygame.time.set_timer(pygame.USEREVENT+1,random.randint(3000,5000)) #bird_spawn
game_active = True
# GAMELOOP ------------------------------------------------
while game:
    clock.tick(80)

    if game_active:
        win.blit(bg,(0,0))
        rubbish_group.draw(win)
        returned_list = loadMap()
        rubbish_group.update()
        plastic_group.draw(win)
        plastic_group.update()
        bin_rect_x = WIDTH-recycling_bin.get_width()
        win.blit(recycling_bin,(bin_rect_x,250))
        bin_rect = pygame.Rect(bin_rect_x,250,50,50)
        player.draw(win)
        player.update()
        bird_group.draw(win)
        bird_group.update()
        renderText(msg='Press ENTER to restart',font=PANEL_FONT,color=(0,0,0),x=10,y=10)
        if pygame.sprite.spritecollide(player.sprite,rubbish_group,True,pygame.sprite.collide_mask):
            score += 1
            collect.play()
        if pygame.sprite.spritecollide(player.sprite,plastic_group,True,pygame.sprite.collide_mask):
            over = 'lose'
            game_active = False
        if pygame.sprite.spritecollide(player.sprite,bird_group,True,pygame.sprite.collide_mask):
            over = 'lose'
            game_active = False
        for plastic in plastic_group:
            pygame.sprite.spritecollide(plastic,rubbish_group,True,pygame.sprite.collide_mask)
        if player.sprite.rect.top > HEIGHT:
            over = 'lose'
            game_active = False
        if player.sprite.rect.colliderect(bin_rect):
            if abs(player.sprite.rect.bottom - bin_rect.bottom) <= 10:
                over = 'win'
                game_active = False

    else:
        win.fill((0,0,0))
        if over == 'lose':
            renderText(msg='Mission Failed',font=GAME_OVER_FONT,color=(200,200,200),x=(WIDTH//2)-120,y=(HEIGHT//2)-50)
            renderText(msg='Press ENTER to play again',font=PANEL_FONT,color=(200,200,200),x=(WIDTH//2)-120,y=(HEIGHT//2)+100)
        elif over == 'win':
            renderText(msg=f'{score} Rubbish Collected',font=GAME_OVER_FONT,color=(200,200,200),x=(WIDTH//2)-160,y=(HEIGHT//2)-100)
            if score < 5:
                renderText(msg='Not Bad',font=GAME_OVER_FONT,color=(200,200,200),x=(WIDTH//2)-90,y=(HEIGHT//2)-30)
            else:
                renderText(msg='Well Done!',font=GAME_OVER_FONT,color=(200,200,200),x=(WIDTH//2)-90,y=(HEIGHT//2)-30)
            renderText(msg='Press ENTER to play again',font=PANEL_FONT,color=(200,200,200),x=(WIDTH//2)-120,y=(HEIGHT//2)+100)
        key = pygame.key.get_pressed()
        if key[pygame.K_RETURN]:
            game_active = True
            player.empty()
            player = pygame.sprite.GroupSingle(Player())
            rubbish_group.empty()
            for i in range(num_rubbish):
                rubbish_group.add(Rubbish())
            plastic_group.empty()
            for i in range(num_plastic):
                plastic_group.add(Plastic())
            bird_group.empty()
            score = 0

    pygame.display.update()

    # EVENTS ---------------------------------------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_RETURN:
                player.empty()
                player = pygame.sprite.GroupSingle(Player())
                rubbish_group.empty()
                for i in range(num_rubbish):
                    rubbish_group.add(Rubbish())
                plastic_group.empty()
                for i in range(num_plastic):
                    plastic_group.add(Plastic())
                score = 0
                bird_group.empty()

        if event.type == pygame.USEREVENT+1:
            bird_group.add(Bird())
