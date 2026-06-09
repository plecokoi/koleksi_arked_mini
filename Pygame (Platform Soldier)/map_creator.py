import pygame,sys,pickle
pygame.init()

# set up
WIDTH,HEIGHT = 980,580
win = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Map Creator")


# functions
def loadImg(path):
    return pygame.image.load('Assets/'+path+'.png').convert_alpha()
def scale(name,size1,size2):
    return pygame.transform.scale(name,(size1,size2))
def text(msg,x,y,color,font,size):
    style = pygame.font.SysFont(font,size)
    textmsg = style.render(msg,1,color)
    return win.blit(textmsg,(x,y))


GAME_WIDTH = 704
GAME_HEIGHT = 480
TILE_SIZE = 32
NUM_TILES_PER_ROW = 15
NUM_TILES_PER_COL = 42
scroll = 0
scroll_left = False
scroll_right = False
scroll_speed = 1
level = 0
img1 = loadImg('Tiles/0')
img2 = loadImg('Tiles/1')
img3 = loadImg('Tiles/2')
img4 = loadImg('Tiles/3')
img5 = loadImg('Tiles/4')
img6 = loadImg('Tiles/5')
img7 = loadImg('Tiles/6')
img8 = loadImg('Tiles/7')
img9 = loadImg('Tiles/8')
imga = loadImg('Tiles/item_ammo')
imgm = loadImg('Tiles/item_medic')
imgg = loadImg('Tiles/item_grenade')
imge = loadImg('Enemy/Idle/0')
img_list = []
for x in range(9):
    img = loadImg(f'Tiles/{x}')
    img_list.append(img)
img_list.append(imga)
img_list.append(imgm)
img_list.append(imgg)
img_list.append(imge)
bg1 = loadImg('Background/sky_cloud')
bg2 = loadImg('Background/mountain')
bg3 = loadImg('Background/pine1')
bg4 = loadImg('Background/pine2')
save_img = loadImg('Tiles/save_btn')
load_img = loadImg('Tiles/load_btn')

world_data = []
for row in range (NUM_TILES_PER_ROW):
    cols = [-1]*NUM_TILES_PER_COL
    world_data.append(cols)

for tile in range(0,NUM_TILES_PER_COL):
    world_data[NUM_TILES_PER_ROW-1][tile] = 0


class Button():
    def __init__(self,x,y,image) -> None:
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

        win.blit(self.image,self.rect)

        return action


def draw_grid():
    for i in range(NUM_TILES_PER_COL+1):
        pygame.draw.line(win,(200,200,200),(i*TILE_SIZE-scroll,0),(i*TILE_SIZE-scroll,GAME_HEIGHT))
    for i in range(NUM_TILES_PER_ROW+1):
        pygame.draw.line(win,(200,200,200),(0,i*TILE_SIZE),(GAME_WIDTH,i*TILE_SIZE))


def background():
    win.fill((144,202,120))
    for x in range(3):
        win.blit(bg1,((x*bg1.get_width())-scroll,0))
        win.blit(bg2,((x*bg1.get_width())-scroll,100))
        win.blit(bg3,((x*bg1.get_width())-scroll,190))
        win.blit(bg4,((x*bg1.get_width())-scroll,260))


def buttons_area():
    pygame.draw.rect(win,(60,140,60),pygame.Rect(GAME_WIDTH,0,WIDTH-GAME_WIDTH,HEIGHT))
    pygame.draw.rect(win,(60,140,60),pygame.Rect(0,GAME_HEIGHT,WIDTH,HEIGHT-GAME_HEIGHT))


def draw_world():
    for y, row in enumerate(world_data):
        for x, tile in enumerate(row):
            if tile >= 0:
                win.blit(img_list[tile],(x*TILE_SIZE-scroll,y*TILE_SIZE))


save_button = Button(400,HEIGHT-70,save_img)
save_rect = pygame.Rect(400,HEIGHT-70,save_img.get_width(),save_img.get_height())
load_button = Button(500,HEIGHT-70,load_img)
load_rect = pygame.Rect(500,HEIGHT-70,save_img.get_width(),load_img.get_height())
button_list = []
btn_col = 0
btn_row = 0
for i in range(len(img_list)):
    tile_button = Button(GAME_WIDTH+(75*btn_col)+50,75*btn_row+50,img_list[i])
    button_list.append(tile_button)
    btn_col += 1
    if btn_col == 3:
        btn_row += 1
        btn_col = 0
current_tile = 0


run = True
clock = pygame.time.Clock()

while run:

    clock.tick(20)

    background()
    draw_grid()
    draw_world()
    buttons_area()
    text(f'Level: {level}',10,HEIGHT-70,(0,0,0),'comicsans',25)
    text('Press UP or DOWN to change level',10,HEIGHT-40,(0,0,0),'comicsans',25)

    if save_button.draw():
        pickle_out = open(f'level{level}', 'wb')
        pickle.dump(world_data,pickle_out)
        pickle_out.close()
                
    if load_button.draw():
        scroll = 0
        world_data = []
        pickle_in = open(f'level{level}', 'rb')
        world_data = pickle.load(pickle_in)
            
    btn_counter = 0
    for btn_counter,i in enumerate (button_list):
        if i.draw():
            current_tile = btn_counter
    pygame.draw.rect(win,(200,20,20),button_list[current_tile],3)


    if scroll_left and scroll>0:
        scroll -= 30 *scroll_speed
    if scroll_right and scroll<(NUM_TILES_PER_COL*TILE_SIZE)-GAME_WIDTH:
        scroll += 30 * scroll_speed

    pos = pygame.mouse.get_pos()
    if save_rect.collidepoint(pos):
        pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND))
    elif load_rect.collidepoint(pos):
        pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND))
    else:
        pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW))
    x = (pos[0]+scroll)//TILE_SIZE
    y = (pos[1])//TILE_SIZE

    if pos [0] < GAME_WIDTH and pos[1] < GAME_HEIGHT:
        if pygame.mouse.get_pressed()[0] == 1:
            if world_data[y][x] != current_tile:
                world_data[y][x] = current_tile
        if pygame.mouse.get_pressed()[2] == 1:
            world_data[y][x] = -1

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_LEFT:
                scroll_left = True
            if event.key == pygame.K_RIGHT:
                scroll_right = True
            if event.key == pygame.K_RSHIFT:
                scroll_speed = 3
            if event.key == pygame.K_UP:
                level += 1
            if event.key == pygame.K_DOWN and level > 0:
                level -= 1

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                scroll_left = False
            if event.key == pygame.K_RIGHT:
                scroll_right = False
            if event.key == pygame.K_RSHIFT:
                scroll_speed = 1
            

