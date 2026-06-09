import pygame,sys,random
pygame.font.init()
pygame.init()
#----------------------------------------------------------------------------------
win = pygame.display.set_mode((500,300))
pygame.display.set_caption("Dino")
#----------------------------------------------------------------------------------
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,150,0)
BLUE = (0,0,150)
LIGHT_GREY = (211,211,211)
LIGHT_BLUE = (0,171,240)
LIGHT_ORANGE = (255,139,40)
LIGHTER_BLUE = (100,180,250)
#----------------------------------------------------------------------------------
dino_font = pygame.font.SysFont('courier new',60)
start_font = pygame.font.SysFont('arial',30)
pause_font = pygame.font.SysFont('times new roman',20)
keys_font = pygame.font.SysFont('arial',30)
about_font = pygame.font.SysFont('courier new',25)
about_smaller_font = pygame.font.SysFont('courier new',20)
restart_font = pygame.font.SysFont('comicsans',20)
score_font = pygame.font.SysFont('courier new',20)
#----------------------------------------------------------------------------------

bg_music = pygame.mixer.Sound ('Assets\music.wav')
bg_music.play(loops=-1)
bg_music.set_volume(0.08)
#----------------------------------------------------------------------------------
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_1 = pygame.image.load("Assets\\1.png")
        player_2 = pygame.image.load("Assets\\2.png")
        player_3 = pygame.image.load("Assets\\3.png")
        self.player_walk = [player_1,player_2,player_3]
        self.player_index = 0
        self.image = self.player_walk[self.player_index]
        self.jump_image = pygame.image.load("Assets\\1.png")
        self.rect = self.image.get_rect(center = (70,185))
        self.mask = pygame.mask.from_surface(self.image)
        self.gravity = 0
        self.jump_music = pygame.mixer.Sound("Assets\\audio_jump.mp3")

    def animation(self):
        if self.rect.bottom < 220:
            self.image = self.jump_image
        else:
            self.player_index += 1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def input(self):
        keys = pygame.key.get_pressed()
        if keys [pygame.K_SPACE] and self.rect.bottom >= 220:
            self.jump_music.play()
            self.jump_music.set_volume(0.2)
            self.gravity = -15
        if keys [pygame.K_UP] and self.rect.bottom >= 220:
            self.jump_music.play()
            self.jump_music.set_volume(0.2)
            self.gravity = -15
        if keys [pygame.K_w] and self.rect.bottom >= 220:
            self.jump_music.play()
            self.jump_music.set_volume(0.2)     
            self.gravity = -15

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 220:
            self.rect.bottom = 220

    def update(self):
        self.input()
        self.apply_gravity()
        self.animation()
#----------------------------------------------------------------------------------
class Obstacles(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()

        if type == "fly":
            fly1 = pygame.image.load("Assets\\Fly1.png")
            fly2 = pygame.image.load("Assets\\Fly2.png")
            self.frames = [fly1,fly2]
            y_pos = 70

        else:
            snail1 = pygame.image.load("Assets\\snail1.png")
            snail2 = pygame.image.load("Assets\\snail2.png")
            self.frames = [snail1,snail2]
            y_pos = 220

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(midbottom = (520,y_pos))

    def animation(self):
        self.animation_index += 0.1 
        if self.animation_index >= len(self.frames): 
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]
        self.rect.x -= 10

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

    def update(self):
        self.animation()
        self.destroy()
#----------------------------------------------------------------------------------
def main_menu():
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(70)

        main_img = pygame.image.load("Assets\\main.png")
        main_img = pygame.transform.scale (main_img,(140,100))
        dino_title = dino_font.render("Dino Game",1,BLACK)
        start_button = pygame.Rect(195,220,100,50)
        start_title = start_font.render("START",1,BLACK)
        help_button = pygame.Rect(55,220,100,50)
        help_title = start_font.render("HELP",1,BLACK)
        about_button = pygame.Rect(335,220,100,50)
        about_title = start_font.render("ABOUT",1,BLACK)

        win.fill(LIGHT_GREY)
        win.blit(main_img,(170,100))
        win.blit(dino_title,(95,30))
        pygame.draw.rect(win,LIGHT_BLUE,start_button)
        win.blit(start_title,(207,227))
        pygame.draw.rect(win,LIGHT_ORANGE,help_button)
        win.blit(help_title,(73,227))
        pygame.draw.rect(win,LIGHT_ORANGE,about_button)
        win.blit(about_title,(343,227))

        pygame.display.update()

        mouse_pos = pygame.mouse.get_pos()
        if start_button.collidepoint(mouse_pos):
            pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND))
        elif help_button.collidepoint(mouse_pos):
            pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND))
        elif about_button.collidepoint(mouse_pos):
            pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND))
        else:
            pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW))
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_p:
                    pause()
                if event.key == pygame.K_h:
                    help_menu()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if start_button.collidepoint(mouse_pos):
                    game()
                if help_button.collidepoint(mouse_pos):
                    help_menu()
                if about_button.collidepoint(mouse_pos):
                    about()
#----------------------------------------------------------------------------------
def about():
    clock = pygame.time.Clock()
    run = True
    while run:
        pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW))
        clock.tick(70)

        about_block = pygame.Rect(10,10,480,280)
        about_block_title = dino_font.render("ABOUT",1,BLACK)
        how_block = pygame.Rect(21,70,455,205)
        how_to_play = about_font.render("How to play :",1,GREEN)
        how_to_play2 = about_smaller_font.render("Jump over and avoid the obstacles",1,BLUE)
        by1 = about_font.render("Game by :",1,GREEN)
        by2 = about_font.render("Darshini",1,BLUE)
        midline = pygame.Rect(21,180,455,2)
        line1 = pygame.Rect(21,70,455,2)
        line2 = pygame.Rect(21,275,455,2)
        line3 = pygame.Rect(21,70,2,205)
        line4 = pygame.Rect(476,71,2,205)

        win.fill(LIGHT_GREY)
        pygame.draw.rect(win,LIGHTER_BLUE,about_block)
        pygame.draw.rect(win,WHITE,how_block)
        pygame.draw.rect(win,BLACK,line1)
        pygame.draw.rect(win,BLACK,line2)
        pygame.draw.rect(win,BLACK,line3)
        pygame.draw.rect(win,BLACK,line4)
        pygame.draw.rect(win,BLACK,midline)
        win.blit(about_block_title,(165,10))
        win.blit(how_to_play,(160,95))
        win.blit(how_to_play2,(50,140))
        win.blit(by1,(195,200))
        win.blit(by2,(200,235))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu()
                if event.key == pygame.K_p:
                    pause()
                if event.key == pygame.K_h:
                    help_menu()
#----------------------------------------------------------------------------------
def help_menu():
    clock = pygame.time.Clock()
    helping = True
    while helping:
        pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW))
        clock.tick(70)
        
        p_key = pygame.image.load("Assets\\p.png")
        p_key = pygame.transform.scale(p_key,(45,45))
        w_key = pygame.image.load("ssets\\w.png")
        w_key = pygame.transform.scale(w_key,(45,45))
        up_key = pygame.image.load("Assets\\up.png")
        up_key = pygame.transform.scale(up_key,(45,45))
        space_key = pygame.image.load("Assets\\space.png")
        space_key = pygame.transform.scale(space_key,(45,45))
        h_key = pygame.image.load("Assets\\h.png")
        h_key = pygame.transform.scale(h_key,(45,45))
        esc_key = pygame.image.load("Assets\\escape.png")
        esc_key = pygame.transform.scale(esc_key,(45,45))

        help_block = pygame.Rect(10,10,480,280)
        keys_block = pygame.Rect(20,70,455,205)
        help_block_title = dino_font.render("HELP",1,BLACK)
        keys_title_pause = keys_font.render("Pause",1,BLACK)
        keys_title_jump = keys_font.render("Jump",1,BLACK)
        keys_title_menu = keys_font.render("Return To Menu",1,BLACK)
        keys_title_help = keys_font.render("Help",1,BLACK)
        line1 = pygame.Rect(20,122,455,2)
        line2 = pygame.Rect(20,172,455,2)
        line3 = pygame.Rect(20,222,455,2)
        line5 = pygame.Rect(20,70,2,205)
        line6 = pygame.Rect(475,70,2,205)
        line7 = pygame.Rect(20,70,455,2)
        line8 = pygame.Rect(20,275,457,2)
        line9 = pygame.Rect(230,70,2,205)


        win.fill(LIGHT_GREY)
        pygame.draw.rect(win,LIGHTER_BLUE,help_block)
        win.blit(help_block_title,(170,10))
        pygame.draw.rect(win,WHITE,keys_block)
        pygame.draw.rect(win,BLACK,line1)
        pygame.draw.rect(win,BLACK,line2)
        pygame.draw.rect(win,BLACK,line3)
        pygame.draw.rect(win,BLACK,line5)
        pygame.draw.rect(win,BLACK,line6)
        pygame.draw.rect(win,BLACK,line7)
        pygame.draw.rect(win,BLACK,line8)
        pygame.draw.rect(win,BLACK,line9)
        win.blit(keys_title_pause,(85,80))
        win.blit(keys_title_jump,(90,127))
        win.blit(keys_title_menu,(35,228))
        win.blit(keys_title_help,(95,177))
        win.blit(p_key,(250,75))
        win.blit(w_key,(250,125))
        win.blit(up_key,(330,125))
        win.blit(space_key,(410,125))
        win.blit(esc_key,(250,227))
        win.blit(h_key,(250,175))
        
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu()
                if event.key == pygame.K_p:
                    pause()
                if event.key == pygame.K_h:
                    helping = False
#----------------------------------------------------------------------------------
def pause():
    pause = True
    while pause:
        pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW))
        pause_text = pause_font.render('Paused',1,BLACK)
        win.blit(pause_text,(440,10))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_p:
                    pause = False
#----------------------------------------------------------------------------------
def game():
    game_active = True
    player = pygame.sprite.GroupSingle(Player())
    obstacles_group = pygame.sprite.Group()
    obstacles_timer = pygame.USEREVENT+2
    pygame.time.set_timer(obstacles_timer,random.randint(1500,1600))
    time_delay = 1000
    timer_event = pygame.USEREVENT + 1
    pygame.time.set_timer(timer_event,time_delay)
    counter = 0
    clock = pygame.time.Clock()
    run = True
    passed = False

    while run:
        pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW))
        clock.tick(50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu()
                if event.key == pygame.K_p:
                    pause()
                if event.key == pygame.K_h:
                    help_menu()

            if game_active:
                if event.type == obstacles_timer:
                    obstacles_group.add(Obstacles(random.choice(['fly','snail','snail'])))
            else:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    game_active = True
                    game()
                    
        if game_active:
            bg_img = pygame.image.load("Assets\\Sky.png")
            ground_img = pygame.image.load("Assets\\ground.png")
            win.blit(bg_img,(0,0))
            win.blit(ground_img,(0,220))
            obstacles_group.draw(win)
            obstacles_group.update()
            player.draw(win)
            player.update()
            if len (obstacles_group.sprites()) > 0:
                if abs(player.sprite.rect.left - obstacles_group.sprites()[0].rect.right)<5:
                    passed = True
                else:
                    passed = False
            if passed:
                counter += 1
            timer = score_font.render(f'Score: {counter}',1,BLACK)
            win.blit(timer,(190,10))
            pygame.display.update()
            if pygame.sprite.spritecollide(player.sprite,obstacles_group,False,pygame.sprite.collide_mask):
                game_active = False

        else: 
            win.fill(LIGHT_GREY)
            score_title = dino_font.render("Score: "+str(counter),1,BLACK)
            space_title = restart_font.render('Press ENTER to restart',1,BLACK)
            escape_title = restart_font.render('Press ESCAPE to return to menu',1,BLACK)
            win.blit(score_title,(90,50))
            win.blit(space_title,(135,200))
            win.blit(escape_title,(95,250))
            pygame.display.update()
#----------------------------------------------------------------------------------
if __name__ == "__main__":
    main_menu()
