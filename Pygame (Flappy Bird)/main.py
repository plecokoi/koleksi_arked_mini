import pygame,sys,random
pygame.init()
#----------------------------------------------------------------------------
WIDTH,HEIGHT = 420,560
win = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Flappy Bird")
#----------------------------------------------------------------------------
BLACK = (0,0,0)
#----------------------------------------------------------------------------
start_font = pygame.font.SysFont('courier new',20)
score_font = pygame.font.SysFont('Bauhaus 93',30)
over_font = pygame.font.SysFont('courier new',50)
#----------------------------------------------------------------------------
bg_img = pygame.image.load(r'Assets\\bg.png')
bg_img = pygame.transform.scale(bg_img,(WIDTH,HEIGHT))
ground_img = pygame.image.load(r'Assets\\ground.png')
flying = False
#----------------------------------------------------------------------------
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        img1 = pygame.image.load(r'Assets\\bird1.png')
        img2 = pygame.image.load(r'Assets\\bird2.png')
        img3 = pygame.image.load(r'Assets\\bird3.png')
        self.flying_img = [img1,img2,img3]
        self.index = 0
        self.image = self.flying_img [self.index]
        self.rect = self.image.get_rect (center = (60,250))
        self.mask = pygame.mask.from_surface(self.image)
        self.gravity = 0

    def animation(self):
        self.index += 0.3
        if self.index >= len(self.flying_img):
            self.index = 0
        self.image = pygame.transform.rotate(self.flying_img[int(self.index)],-10)

    def player_gravity(self):
        global flying 
        if flying == True:
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE] and self.rect.y > 10:
                self.gravity = -4
                self.image = pygame.transform.rotate(self.flying_img[int(self.index)],10)
            self.gravity += 0.4
            self.rect.y += self.gravity

    def update(self):
        self.animation()
        self.player_gravity()
#----------------------------------------------------------------------------
class Pipes(pygame.sprite.Sprite):
    def __init__(self,position,x,y):
        super().__init__()
        self.image = pygame.image.load(r'Assets\\pipe.png')
        self.vel = 5
        self.pipegap = 150
        if position == 1:
            self.image = pygame.transform.flip(self.image,False,True)
            self.rect = self.image.get_rect (bottomleft = (x,y-int(self.pipegap/2)))
            self.mask = pygame.mask.from_surface(self.image)
        if position == -1:
            self.rect = self.image.get_rect (topleft = (x,y+int(self.pipegap/2)))
            self.mask = pygame.mask.from_surface(self.image)
 
    def movement(self):
        if flying == True:
            self.rect.x -= self.vel
            if self.rect.x + self.rect.width <= 0:
                self.kill()

    def update(self):
        self.movement()
#----------------------------------------------------------------------------      
def game():
    clock = pygame.time.Clock()
    run = True
    player = pygame.sprite.GroupSingle(Player()) 
    top_pipe = pygame.sprite.Group()
    bottom_pipe = pygame.sprite.Group()
    pygame.time.set_timer(pygame.USEREVENT+1,random.randint(1000,2500))
    pygame.time.set_timer(pygame.USEREVENT+2,1000)
    counter = 0
    playing = False
    pass_pipe = False
    bgX1 = 0
    bgX2 = ground_img.get_width()
    over = False

    while run:
        clock.tick(70)
        global flying

        win.blit(bg_img,(0,0))
        space_start = start_font.render("Press SPACE to start",1,BLACK)
        win.blit(space_start,(90,100))
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            playing = True
        if playing == True:
            win.blit(bg_img,(0,0))
        else:
            player.sprite.image = pygame.transform.rotate(player.sprite.flying_img[int(player.sprite.index)],0)
        player.draw(win)
        player.update()
        top_pipe.draw(win)
        top_pipe.update()
        bottom_pipe.draw(win)
        bottom_pipe.update()

        bgX1 -= 5
        bgX2 -= 5
        bgrect = ground_img.get_rect()
        if bgX1 <= -bgrect.width:
            bgX1 = bgrect.width
        if bgX2 <= -bgrect.width:
            bgX2 = bgrect.width
        win.blit(ground_img, (bgX1, HEIGHT-100))
        win.blit(ground_img, (bgX2, HEIGHT-100))

        if pygame.sprite.spritecollide(player.sprite,top_pipe,False,pygame.sprite.collide_mask):
            over = True
            flying = False
            win.blit(ground_img,(0,HEIGHT-100))
            restart_button = pygame.image.load(r'Assets\\restart.png')
            x = 140
            y = 270
            width = restart_button.get_width()
            height = restart_button.get_height()
            restart_rect = pygame.Rect(x,y,width,height)
            win.blit(restart_button,(x,y))
            score_msg = over_font.render("SCORE:"+str(counter),1,BLACK)
            win.blit(score_msg,(90,200))
            mouse_pos = pygame.mouse.get_pos()
            if restart_rect.collidepoint(mouse_pos):
                pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND))
            else:
                pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW))
            
        if pygame.sprite.spritecollide(player.sprite,bottom_pipe,False,pygame.sprite.collide_mask):
            over = True
            flying = False
            win.blit(ground_img,(0,HEIGHT-100))
            restart_button = pygame.image.load(r'Assets\\restart.png')
            x = 140
            y = 270
            width = restart_button.get_width()
            height = restart_button.get_height()
            restart_rect = pygame.Rect(x,y,width,height)
            win.blit(restart_button,(x,y))
            score_msg = over_font.render("SCORE:"+str(counter),1,BLACK)
            win.blit(score_msg,(90,200))
            mouse_pos = pygame.mouse.get_pos()
            if restart_rect.collidepoint(mouse_pos):
                pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND))
            else:
                pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW))

        if len(top_pipe) > 0:
            if player.sprite.rect.left > top_pipe.sprites()[0].rect.left and player.sprite.rect.right < top_pipe.sprites()[0].rect.right and pass_pipe == False:
                pass_pipe = True
            if pass_pipe == True:
                if player.sprite.rect.left > top_pipe.sprites()[0].rect.right:
                    counter += 1
                    pass_pipe = False

        ground_y = 470
        if player.sprite.rect.bottom >= ground_y:
            player.sprite.rect.bottom = ground_y
            player.sprite.image = pygame.transform.rotate(player.sprite.flying_img[0],-45)
            over = True
            flying = False
            win.blit(ground_img,(0,HEIGHT-100))
            restart_button = pygame.image.load(r'Assets\\restart.png')
            x = 140
            y = 270
            width = restart_button.get_width()
            height = restart_button.get_height()
            restart_rect = pygame.Rect(x,y,width,height)
            win.blit(restart_button,(x,y))
            score_msg = over_font.render("SCORE:"+str(counter),1,BLACK)
            win.blit(score_msg,(90,200))
        
            mouse_pos = pygame.mouse.get_pos()
            if restart_rect.collidepoint(mouse_pos):
                pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND))
            else:
                pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW))

        score = score_font.render(str(counter),1,BLACK)
        win.blit(score,(200,10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_SPACE and flying == False and over==False:
                    flying = True

            if event.type == pygame.USEREVENT+1 and playing == True:
                pipe_height = random.randint(-100,70)
                top_pipe.add(Pipes(1,500,int(HEIGHT/2)+pipe_height))
                bottom_pipe.add(Pipes(-1,500,int(HEIGHT/2)+pipe_height))

            if event.type == pygame.MOUSEBUTTONDOWN and event.button ==1:
                mouse_pos = pygame.mouse.get_pos()
                if restart_rect.collidepoint(mouse_pos):
                    pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW))
                    game()

        pygame.display.update()
#----------------------------------------------------------------------------
if __name__ == "__main__":
    game()
