import pygame,sys,random,time
pygame.init()

WIDTH,HEIGHT = 902,481
win = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Snake Game")

block_size = 10
SNAKE_COLOR = (20,255,20)
BG_COLOR = (0,0,0)
APPLE_COLOR = (255,20,20)
SCORE_COLOR = (255,255,255)
BTN_COLOR = (25,189,255)
MAINTITLE_FONT = pygame.font.SysFont('comic sans',100)
SCORE_FONT = pygame.font.SysFont('candara',30)
PAUSE_FONT = pygame.font.SysFont('candara',20)
FINAL_FONT = pygame.font.SysFont('candara',50)
RESTART_FONT = pygame.font.SysFont('candara',30,True)
hit_audio = pygame.mixer.Sound('Assets\\snake_hit.mp3')
move_audio = pygame.mixer.Sound('Assets\\move.mp3')
munch_audio = pygame.mixer.Sound('Assets\\munch.mp3')

class Snake():
    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect((WIDTH//block_size)*(block_size//2) , (HEIGHT//block_size)*(block_size/2) , block_size,block_size)
        self.x_dir = 1*block_size
        self.y_dir = 0

    def draw(self,snake_list):
        for x in snake_list:
            pygame.draw.rect(win,SNAKE_COLOR,pygame.Rect(x[0],x[1],block_size,block_size))
        
    def boundaries(self,score):
        if self.rect.right >= ((WIDTH//block_size)*(block_size))+2: #right
            hit_audio.play()
            time.sleep(2)
            game_over(msg="You hit the wall",final_score=score)
        if self.rect.bottom > (HEIGHT//block_size)*(block_size): #down
            hit_audio.play()
            time.sleep(2)
            game_over(msg="You hit the wall",final_score=score)
        if self.rect.y <= -10: #up
            hit_audio.play()
            time.sleep(2)
            game_over (msg="You hit the wall",final_score=score)
        if self.rect.x <= -5: #left
            hit_audio.play()
            time.sleep(2)
            game_over(msg="You hit the wall",final_score=score)

class Food():
    def __init__(self):
        self.x_pos = random.randint(1,(WIDTH//block_size)-2)
        self.y_pos = random.randint(1,(HEIGHT//block_size)-2)
        self.rect = pygame.Rect((self.x_pos*block_size),(self.y_pos*block_size),block_size,block_size)

    def draw(self):
        pygame.draw.rect(win,APPLE_COLOR,self.rect)

def scoring(score):
    score_title = SCORE_FONT.render("Score: "+str(score),1,SCORE_COLOR)
    win.blit(score_title,(10,10))
    pause_title = PAUSE_FONT.render('Press P to PAUSE',1,SCORE_COLOR)
    win.blit(pause_title,(WIDTH-pause_title.get_width()-10,10))

def main_menu():
    clock = pygame.time.Clock()
    run = True

    while run:
        
        clock.tick(70)

        win.fill(BG_COLOR)
        title = MAINTITLE_FONT.render("Snake  Game",1,SCORE_COLOR)
        win.blit(title,((WIDTH/2)-220,150))
        play_btn = pygame.Rect((WIDTH/2)-82,300,150,50)
        pygame.draw.rect(win,BTN_COLOR,play_btn,border_radius=25)
        btn_desc = RESTART_FONT.render("PLAY",1,BG_COLOR)
        win.blit(btn_desc,((WIDTH/2)-41,312))
        pygame.display.update()

        mouse_pos = pygame.mouse.get_pos()
        if play_btn.collidepoint(mouse_pos):
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

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if play_btn.collidepoint(mouse_pos):
                    game()


def pause():
    clock = pygame.time.Clock()
    pause = True

    while pause:
        clock.tick(70)

        win.fill(BG_COLOR)
        pause_notice = FINAL_FONT.render("Paused",1,SCORE_COLOR)
        win.blit(pause_notice,(375,50))

        resume_img = pygame.image.load('Assets\\resume.png')
        resume_img = pygame.transform.scale(resume_img,(190,80))
        resume_rect = pygame.Rect(360,160,190,80)
        win.blit(resume_img,(360,160))
        
        restart_img = pygame.image.load('Assets\\restart.png')
        restart_img = pygame.transform.scale(restart_img,(190,80))
        restart_rect = pygame.Rect(360,260,190,80)
        win.blit(restart_img,(360,260))

        menu_img = pygame.image.load('Assets\\menu.png')
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
    snake = Snake()
    food = Food()
    snake_list = []
    snake_length = 0
    eaten = 0

    while run:
        pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW))
        clock.tick(30)

        win.fill(BG_COLOR)
            
        snake_head = []
        snake_head.append(snake.rect.x)
        snake_head.append(snake.rect.y)
        snake_list.append(snake_head)
        food.draw()
        snake.draw(snake_list)
        snake.boundaries(eaten)

        if snake.rect.colliderect(food.rect):
            munch_audio.play()
            x_pos = ((random.randint(1,(WIDTH//block_size)-2))*block_size)
            y_pos = ((random.randint(1,(HEIGHT//block_size)-2))*block_size)
            food.rect.x = x_pos
            food.rect.y = y_pos
            snake_length+=1
            eaten += 1

        snake.rect.x += snake.x_dir
        snake.rect.y += snake.y_dir

        for snake_body in snake_list[:-1]:
            if snake_body==snake_head:
                hit_audio.play()
                time.sleep(2)
                game_over(msg="You hit yourself",final_score=eaten)

        for snake_head in snake_list:
            pygame.draw.rect(win,(10,170,10),pygame.Rect(snake.rect.x,snake.rect.y,block_size,block_size))

        if len(snake_list)>snake_length:
            del snake_list[0]

        scoring(eaten)
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

                if event.key == pygame.K_LEFT:
                    move_audio.play()
                    snake.x_dir = -1*block_size
                    snake.y_dir = 0
                if event.key == pygame.K_RIGHT:
                    move_audio.play()
                    snake.x_dir = 1*block_size
                    snake.y_dir = 0
                if event.key == pygame.K_UP:
                    move_audio.play()
                    snake.y_dir = -1*block_size
                    snake.x_dir = 0
                if event.key == pygame.K_DOWN:
                    move_audio.play()
                    snake.y_dir = 1*block_size
                    snake.x_dir = 0

        pygame.time.wait(60)

def game_over(msg,final_score):
    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(10)

        win.fill(BG_COLOR)
        message = SCORE_FONT.render(msg,1,SCORE_COLOR)
        win.blit(message,((WIDTH/2)-100,100))
        total_score = FINAL_FONT.render("Score: "+str(final_score),1,SCORE_COLOR)
        win.blit(total_score,((WIDTH/2)-90,200))
        restart_btn = pygame.Rect((WIDTH/2)-80,300,150,50)
        pygame.draw.rect(win,BTN_COLOR,restart_btn,border_radius=25)
        btn_desc = RESTART_FONT.render("RESTART",1,BG_COLOR)
        win.blit(btn_desc,((WIDTH/2)-64,312))
        pygame.display.update()

        mouse_pos = pygame.mouse.get_pos()
        if restart_btn.collidepoint(mouse_pos):
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
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if restart_btn.collidepoint(mouse_pos):
                    game()

if __name__=="__main__":
    main_menu()