from appModules import pygame, os, random
from assets import RED_SPACE_SHIP, GREEN_SPACE_SHIP, BLUE_SPACE_SHIP, YELLOW_SPACE_SHIP
from assets import RED_LASER, GREEN_LASER, BLUE_LASER, YELLOW_LASER, BG, WIDTH_SCREEN, HEIGHT_SCREEN
from Model.player import Player
from Model.enemy import Enemy
from interfaces.colision import collide
from pocketsphinx import LiveSpeech


import serial
import codecs  



#arduino = serial.Serial(port='COM3', baudrate=115200, timeout=.1)
####################### Seting main variables ######################
pygame.font.init()
WIN = pygame.display.set_mode((WIDTH_SCREEN, HEIGHT_SCREEN))
pygame.display.set_caption("Navs invader - Audio Recognition")
## Game Vars
###################################################################
PLAYER_VEL = 5
BEGIN_SCREEN = 0
player = Player( 300, 505)
###################################################################
#Model
#https://stackoverflow.com/questions/39907245/how-can-i-configure-spanish-in-pocketsphinx-with-python
#ARDUINO VARS
NAV_IZQUIERDA = False
NAV_DERECHA = False
NAV_LASER = False
#BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")), (WIDTH_SCREEN, HEIGHT_SCREEN))


def get_arduino_data():   
    data = arduino.readline()
    return data


def init_enviroment():    
    game_vars = {
        "run" :True,
        "FPS" : 60,
        "level": 0,
        "lives" : 5,
        "PLAYER_VEL": 5,
        "ENEMY_VEL" : 1,
        "enemies":[ ] , 
        "lost" : False,
        "lost_count": 0,
        "wave_length":0,
        "laser_vel":4,
        "main_font": pygame.font.SysFont("comicsans", 30),
        "lost_font": pygame.font.SysFont("comicsans", 30),
        "clock": pygame.time.Clock()
    }
    return game_vars

def arduino_decision():
    NEXT_PLAYER_LEFT_X_POSITION = player.x - PLAYER_VEL
    NEXT_PLAYER_RIGHT_X_POSITION = player.x + PLAYER_VEL + player.get_width()
    
    word = get_arduino_data()
    word = codecs.decode(word, 'UTF-8')
    if(len(word) > 0):
        print(word)
        global NAV_IZQUIERDA
        global NAV_DERECHA
        global NAV_LASER
        if( word == 'izquierda'):
            NAV_IZQUIERDA = True
            NAV_DERECHA = False
            #NAV_LASER = False
        if(word == 'derecha'):
            NAV_DERECHA = True
            NAV_IZQUIERDA = False
            #NAV_LASER = False
        if(word == 'laser'):
            if(NAV_LASER):
                NAV_LASER = False
            else:
                NAV_LASER = True
            """NAV_IZQUIERDA = False
            NAV_DERECHA = False"""         

        if( NAV_IZQUIERDA and (NEXT_PLAYER_LEFT_X_POSITION > BEGIN_SCREEN)):
            player.x -= PLAYER_VEL
        if(NAV_DERECHA and (NEXT_PLAYER_RIGHT_X_POSITION < WIDTH_SCREEN)):
            player.x += PLAYER_VEL
        if(NAV_LASER):
            player.shoot()

def checking_events(player, PLAYER_VEL ):
    NEXT_PLAYER_LEFT_X_POSITION = player.x - PLAYER_VEL
    NEXT_PLAYER_RIGHT_X_POSITION = player.x + PLAYER_VEL + player.get_width()
    NEXT_PLAYER_UP_POSITION = player.y - PLAYER_VEL
    # Diez asociado a la barra de vida
    NEXT_PLAYER_DOWN_POSITION = player.y + PLAYER_VEL + player.get_height() + 20
    #------------------------------------------------------------------------    
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and NEXT_PLAYER_LEFT_X_POSITION > BEGIN_SCREEN:
        player.x -= PLAYER_VEL
    if keys[pygame.K_RIGHT] and NEXT_PLAYER_RIGHT_X_POSITION < WIDTH_SCREEN:
        player.x += PLAYER_VEL
    if keys[pygame.K_UP] and NEXT_PLAYER_UP_POSITION > BEGIN_SCREEN:
        player.y -= PLAYER_VEL
    if keys[pygame.K_DOWN] and NEXT_PLAYER_DOWN_POSITION < HEIGHT_SCREEN:
        player.y += PLAYER_VEL
    if keys[pygame.K_SPACE]:
        player.shoot()

def background_random():
    background = random.choice(["1", "2", "3","4"])
    global BG
    if background == "1":
        BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")), (WIDTH_SCREEN, HEIGHT_SCREEN))
    if background == "2":
        BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "space_1.png")), (WIDTH_SCREEN, HEIGHT_SCREEN))
    if background == "3":
        BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "space_2.png")), (WIDTH_SCREEN, HEIGHT_SCREEN))
    if background == "4":
        BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "space_3.png")), (WIDTH_SCREEN, HEIGHT_SCREEN))

        
def enemy_behavior(game_vars, enemies,ENEMY_VEL,WIN):
    
    if len(enemies) == 0:
        game_vars["level"] = game_vars["level"] + 1        
        game_vars["wave_length"] = game_vars["wave_length"] + 4
        
        background_random()        
        for i in range(game_vars["wave_length"]):  
            agenEnemy = Enemy(random.randrange(50, WIDTH_SCREEN - 90),random.randrange(-1500, -50), random.choice(["red", "green", "blue"]) )
            game_vars['enemies'].append(agenEnemy)

    for enemy in game_vars['enemies']:
        enemy.draw(WIN)
        enemy.move(ENEMY_VEL)
        enemy.move_lasers(game_vars["laser_vel"], player) 

        if random.randrange(0, 2 * game_vars["FPS"]) == 1:
            enemy.shoot()

        if collide(enemy, player):
            player.health -= 10
            enemies.remove(enemy)
        elif enemy.y + enemy.get_height() > HEIGHT_SCREEN:
            #game_vars["lives"] = game_vars["lives"] - 1
            player.health -= 10
            enemies.remove(enemy)

def redraw_windows(WIN, game_vars, WIDTH, player, FPS):
    global BG
    WIN.blit(BG, (0,0))
    lives_label = game_vars['main_font'].render(f"Lives: {game_vars['lives']}",0, (255,255,255))
    level_label = game_vars['main_font'].render(f"Level: {game_vars['level']}",0, (255,255,255))
    

    WIN.blit(lives_label, (10, 10))
    WIN.blit(level_label, (WIDTH - level_label.get_width() - 10 , 10))
    player.draw(WIN)
    if player.health <= 0:
        if game_vars['lives'] <= 0:
            game_vars['lost'] = True
        else:
            game_vars['lives'] = game_vars['lives'] - 1
            player.health = 100

                 
    if game_vars['lives'] <= 0 and player.health <= 0:
        game_vars['lost'] = True
        game_vars['lost_count'] = game_vars['lost_count'] + 1
           
    if game_vars['lost']:
        if game_vars['lost_count'] > game_vars['FPS'] * 3:
            game_vars['run'] = False
        else:
            pass

    if game_vars['lost']:
        lost_label = game_vars['lost_font'].render("you lost!!",1, (255,255,255))
        WIN.blit(lost_label,(WIDTH_SCREEN/2 - lost_label.get_width()/2,350))

    enemy_behavior(game_vars ,game_vars['enemies'], game_vars['ENEMY_VEL'],WIN)    
    player.move_lasers(-game_vars["laser_vel"], game_vars['enemies'])
    #arduino_decision()
    checking_events(player, game_vars['PLAYER_VEL'])
    pygame.display.update()

def worker():
    
    speech = LiveSpeech(lm=False, kws='key.list')
    print('ccoriendo')
    for phrase in speech:
        word = str(phrase.segments(detailed=True)[0][0])
        if (len(word.split()) == 0): break       
        print(word.split()[0])
        break    

def main():    
    game_vars = init_enviroment()
    while game_vars['run']:
        game_vars['clock'].tick(game_vars['FPS'])
        #worker() 
        redraw_windows(WIN, game_vars,  WIDTH_SCREEN, player, game_vars['FPS'] )      
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #game_vars['run'] = False
                quit()

def main_menu():
    global BG
    title_menu = pygame.font.SysFont("comicsans",20)
    run = True    
    while run:
        WIN.blit(BG,(0,0))
        title_menu_label = title_menu.render("Press the mouse to begin . .", 1, (255,255,255))
        WIN.blit(title_menu_label, (WIDTH_SCREEN/2 - title_menu_label.get_width()/2, 350))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
    pygame.quit()


main_menu()




