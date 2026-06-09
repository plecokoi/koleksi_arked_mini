import pygame,sys
pygame.init()
pygame.font.init()

WIDTH,HEIGHT = 900,500
win = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Pong")

BLACK = (0,0,0)
LIGHT_GREY = (211,211,211)
WINNING_FONT = pygame.font.SysFont('verdana',70)
SCORE_FONT = pygame.font.SysFont('comic sans',40)
KEY_FONT = pygame.font.SysFont('MS serif',30)
TITLE_FONT = pygame.font.SysFont('courier new',50)
score_audio = pygame.mixer.Sound(r'Assets\\score_audio.mp3')
paddle_audio = pygame.mixer.Sound(r'Assets\\paddle_audio.mp3')
wall_audio = pygame.mixer.Sound(r'Assets\\wall_audio.mp3')

class LeftPaddle():
    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(5,195,20,100)
        self.vel = 3
        
    def input(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_w] and self.rect.y>0:
            self.rect.y -= self.vel
        if key[pygame.K_s] and self.rect.bottom<500:
            self.rect.y += self.vel

    def draw(self):
        pygame.draw.rect(win,LIGHT_GREY,self.rect)

    def update(self):
        self.input()

class RightPaddle():
    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(875,195,20,100)
        self.vel = 3
        
    def input(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_UP] and self.rect.y>0:
            self.rect.y -= self.vel
        if key[pygame.K_DOWN] and self.rect.bottom<500:
            self.rect.y += self.vel

    def draw(self):
        pygame.draw.rect(win,LIGHT_GREY,self.rect)

    def update(self):
        self.input()

class Ball():
    def __init__(self):
        super().__init__()
        self.respawn_x = 436
        self.respawn_y = 225
        self.rect = pygame.Rect(self.respawn_x,self.respawn_y,30,30)
        self.vel_x = 4
        self.vel_y = 4

    def draw(self):
        pygame.draw.rect(win,LIGHT_GREY,self.rect,border_radius = 100)

    def movement(self):
        self.rect.x += self.vel_x
        self.rect.y -= self.vel_y
        if self.rect.y <= 0 :
            self.vel_y = -self.vel_y
            wall_audio.play()
            wall_audio.set_volume(0.9)

        if self.rect.y + 30 >=500:
            self.vel_y = -self.vel_y
            wall_audio.play()
            wall_audio.set_volume(0.9)

    def update(self):
        self.movement()

def main_menu():
    clock = pygame.time.Clock()
    run = True
    
    while run:
        clock.tick(70)

        win.fill(BLACK)
        main_img = pygame.image.load(r'Assets\main.png')
        main_img = pygame.transform.scale(main_img,(250,250))
        win.blit(main_img,(330,50))

        play_img = pygame.image.load(r'Assets\play.png')
        play_img = pygame.transform.scale(play_img,(190,80))
        play_rect = pygame.Rect(355,360,190,80)
        win.blit(play_img,(355,360))
        
        exit_img = pygame.image.load(r'Assets\exit.png')
        exit_img = pygame.transform.scale(exit_img,(190,80))
        exit_rect = pygame.Rect(630,360,190,80)
        win.blit(exit_img,(630,360))

        help_img = pygame.image.load(r'Assets\help.png')
        help_img = pygame.transform.scale(help_img,(190,80))
        help_rect = pygame.Rect(80,360,190,80)
        win.blit(help_img,(80,360))

        pygame.display.flip()

        if play_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND))
        elif exit_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND))
        elif help_rect.collidepoint(pygame.mouse.get_pos()):
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

                if event.key == pygame.K_h:
                    help_menu()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if play_rect.collidepoint(mouse_pos):
                    game()
                if exit_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()
                if help_rect.collidepoint(mouse_pos):
                    help_menu()
                
def help_menu():
    clock = pygame.time.Clock()
    run = True

    while run:
        pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW))

        clock.tick(70)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    main_menu()

                if event.key == pygame.K_h:
                    run = False

        win.fill(BLACK)

        help_title = TITLE_FONT.render("CONTROLS",1,LIGHT_GREY)
        win.blit(help_title,(120,55))

        how_title = TITLE_FONT.render("HOW TO WIN",1,LIGHT_GREY)
        win.blit(how_title,(530,50))

        credits_title = TITLE_FONT.render("CREATED BY",1,LIGHT_GREY)
        win.blit(credits_title,(523,322))

        credit = TITLE_FONT.render("DARSHINI",1,LIGHT_GREY)
        win.blit(credit,(555,400))

        left_key = KEY_FONT.render("Left Paddle",1,LIGHT_GREY)
        win.blit(left_key,(95,150))

        right_key = KEY_FONT.render("Right Paddle",1,LIGHT_GREY)
        win.blit(right_key,(90,218))

        help_key = KEY_FONT.render("Help",1,LIGHT_GREY)
        win.blit(help_key,(120,288))

        pause_key = KEY_FONT.render("Pause",1,LIGHT_GREY)
        win.blit(pause_key,(115,357))

        menu_key = KEY_FONT.render("Return to menu / Exit",1,LIGHT_GREY)
        win.blit(menu_key,(45,428))

        w_key = KEY_FONT.render("W",1,LIGHT_GREY)
        win.blit(w_key,(310,150))

        s_key = KEY_FONT.render("S",1,LIGHT_GREY)
        win.blit(s_key,(390,150))

        up_key = KEY_FONT.render("UP",1,LIGHT_GREY)
        win.blit(up_key,(305,220))

        down_key = KEY_FONT.render("DOWN",1,LIGHT_GREY)
        win.blit(down_key,(360,220))

        h = KEY_FONT.render("H",1,LIGHT_GREY)
        win.blit(h,(350,288))

        p = KEY_FONT.render("P",1,LIGHT_GREY)
        win.blit(p,(350,357))

        esc = KEY_FONT.render("ESCAPE",1,LIGHT_GREY)
        win.blit(esc,(320,428))

        one_win = KEY_FONT.render("1) Use the paddle to hit the ball back to",1,LIGHT_GREY)
        win.blit(one_win,(480,130))

        onee_win = KEY_FONT.render("your opponent.",1,LIGHT_GREY)
        win.blit(onee_win,(505,155))

        two_win = KEY_FONT.render("2) Get higher score than your opponent",1,LIGHT_GREY)
        win.blit(two_win,(480,210))

        two_win = KEY_FONT.render("in 30 seconds.",1,LIGHT_GREY)
        win.blit(two_win,(505,235))

        pygame.draw.line(win,LIGHT_GREY,(25,38),(25,472),5) #left line
        pygame.draw.line(win,LIGHT_GREY,(270,123),(270,470),5) # middle line
        pygame.draw.line(win,LIGHT_GREY,(24,125),(447,125),5) #top line
        pygame.draw.line(win,LIGHT_GREY,(24,40),(447,40),5) #roof line
        pygame.draw.line(win,LIGHT_GREY,(24,470),(445,470),5) #bottom line
        pygame.draw.line(win,LIGHT_GREY,(445,40),(445,472),5) #right line
        pygame.draw.line(win,LIGHT_GREY,(25,190),(445,190),5) 
        pygame.draw.line(win,LIGHT_GREY,(25,260),(445,260),5) 
        pygame.draw.line(win,LIGHT_GREY,(25,330),(445,330),5) 
        pygame.draw.line(win,LIGHT_GREY,(25,400),(445,400),5) 

        pygame.draw.line(win,LIGHT_GREY,(470,38),(470,270),5) #left
        pygame.draw.line(win,LIGHT_GREY,(469,40),(875,40),5) #roof line
        pygame.draw.line(win,LIGHT_GREY,(469,110),(875,110),5) #top line
        pygame.draw.line(win,LIGHT_GREY,(468,270),(877,270),5) #bottom line
        pygame.draw.line(win,LIGHT_GREY,(875,38),(875,270),5) #right
        
        pygame.draw.line(win,LIGHT_GREY,(470,310),(470,469),5) #left
        pygame.draw.line(win,LIGHT_GREY,(468,310),(877,310),5) #roof line
        pygame.draw.line(win,LIGHT_GREY,(469,385),(875,385),5) #top line
        pygame.draw.line(win,LIGHT_GREY,(468,469),(877,469),5) #bottom line
        pygame.draw.line(win,LIGHT_GREY,(875,310),(875,468),5) #right

        pygame.display.update()

def pause():
    clock = pygame.time.Clock()
    pause = True

    while pause:
        clock.tick(70)

        win.fill(BLACK)
        pause_notice = TITLE_FONT.render("Paused",1,LIGHT_GREY)
        win.blit(pause_notice,(365,50))

        resume_img = pygame.image.load(r'Assets\resume.png')
        resume_img = pygame.transform.scale(resume_img,(190,80))
        resume_rect = pygame.Rect(360,160,190,80)
        win.blit(resume_img,(360,160))
        
        restart_img = pygame.image.load(r'Assets\restart.png')
        restart_img = pygame.transform.scale(restart_img,(190,80))
        restart_rect = pygame.Rect(360,260,190,80)
        win.blit(restart_img,(360,260))

        menu_img = pygame.image.load(r'Assets\menu.png')
        menu_img = pygame.transform.scale(menu_img,(190,80))
        menu_rect = pygame.Rect(360,360,190,80)
        win.blit(menu_img,(360,360))

        if resume_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND))
        elif restart_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND))
        elif menu_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND))
        else:
            pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW))

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    main_menu()

                if event.key == pygame.K_p:
                    pause = False

                if event.key == pygame.K_h:
                    help_menu()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if resume_rect.collidepoint(mouse_pos):
                    pause = False
                if restart_rect.collidepoint(mouse_pos):
                    game()
                if menu_rect.collidepoint(mouse_pos):
                    main_menu()

        pygame.display.update()

def game():
    clock = pygame.time.Clock()
    run = True
    lPaddle = LeftPaddle()
    rPaddle = RightPaddle()
    ball = Ball()
    left_score = 0
    right_score = 0
    game_over = False
    pygame.time.set_timer(pygame.USEREVENT+1,1000)
    counter = 0
    
    while run:
        pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW))
        clock.tick(70)

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

            if event.type == pygame.USEREVENT+1 and int(counter) < 31:
                counter += 1

        win.fill(BLACK)
        pygame.draw.line(win,LIGHT_GREY,(WIDTH//2,0),(WIDTH//2,HEIGHT),2)
        lPaddle.draw()
        lPaddle.update()
        rPaddle.draw()
        rPaddle.update()
        ball.draw()
        ball.update()
        if ball.rect.colliderect(rPaddle.rect):
            if abs(ball.rect.right - rPaddle.rect.left) < 10:
                ball.vel_x = -ball.vel_x
                paddle_audio.play()
        if ball.rect.colliderect(lPaddle.rect):
            if abs(ball.rect.left - lPaddle.rect.right) < 10:
                ball.vel_x =-ball.vel_x
                paddle_audio.play()

        if ball.rect.x < -30:
            ball.rect.x = ball.respawn_x
            ball.rect.y = ball.respawn_y
            score_audio.play()
            right_score += 1
            
        if ball.rect.x > WIDTH:
            ball.rect.x = ball.respawn_x
            ball.rect.y = ball.respawn_y
            score_audio.play()
            left_score += 1

        left_font = SCORE_FONT.render(str(left_score),1,LIGHT_GREY)
        win.blit(left_font,(215,50))
        right_font = SCORE_FONT.render(str(right_score),1,LIGHT_GREY)
        win.blit(right_font,(670,50))
        pygame.draw.rect(win,LIGHT_GREY,pygame.Rect((WIDTH//2)-25,0,70,60))

        countera = 0

        if counter == 0:
            countera = str('00')
        elif counter == 1:
            countera = str('01')
        elif counter == 2:
            countera = str('02')
        elif counter == 3:
            countera = str('03')
        elif counter == 4:
            countera = str('04')
        elif counter == 5:
            countera = str('05')
        elif counter == 6:
            countera = str('06')
        elif counter == 7:
            countera = str('07')
        elif counter == 8:
            countera = str('08')
        elif counter == 9:
            countera = str('09')
            
        else:
            countera = counter
        
        timer = SCORE_FONT.render(str(countera),1,BLACK)
        win.blit(timer,((WIDTH//2)-15,5))

        if counter == 30:
            game_over = True

        if game_over == True and left_score > right_score:
            ball.vel_x = 0
            ball.vel_y = 0
            win.fill(BLACK)
            left_wins = WINNING_FONT.render("Left Player",1,LIGHT_GREY)
            win.blit(left_wins,(270,170))
            wins = WINNING_FONT.render("WINS!",1,LIGHT_GREY)
            win.blit(wins,(330,250))
            space = KEY_FONT.render("Press SPACE to play again.",1,LIGHT_GREY)
            quit_key = KEY_FONT.render("Press ESCAPE to return to menu.",1,LIGHT_GREY)
            win.blit(space,(20,435))
            win.blit(quit_key,(20,465))
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE]:
                game()
            if key[pygame.K_ESCAPE]:
                main_menu()

        elif game_over == True and right_score > left_score:
            ball.vel_x = 0
            ball.vel_y = 0
            win.fill(BLACK)
            right_wins = WINNING_FONT.render("Right Player",1,LIGHT_GREY)
            win.blit(right_wins,(250,170))
            wins = WINNING_FONT.render("WINS!",1,LIGHT_GREY)
            win.blit(wins,(330,250))
            space = KEY_FONT.render("Press SPACE to play again.",1,LIGHT_GREY)
            quit_key = KEY_FONT.render("Press ESCAPE to return to menu.",1,LIGHT_GREY)
            win.blit(space,(20,435))
            win.blit(quit_key,(20,465))
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE]:
                game()
            if key[pygame.K_ESCAPE]:
                main_menu()

        elif game_over == True and left_score == right_score:
            ball.vel_x = 0
            ball.vel_y = 0
            win.fill(BLACK)
            wins = WINNING_FONT.render("IT'S A TIE",1,LIGHT_GREY)
            win.blit(wins,(260,170))
            space = KEY_FONT.render("Press SPACE to play again.",1,LIGHT_GREY)
            quit_key = KEY_FONT.render("Press ESCAPE to return to menu.",1,LIGHT_GREY)
            win.blit(space,(20,435))
            win.blit(quit_key,(20,465))
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE]:
                game()
            if key[pygame.K_ESCAPE]:
                main_menu()

        pygame.display.flip()

if __name__=="__main__":
    main_menu()
