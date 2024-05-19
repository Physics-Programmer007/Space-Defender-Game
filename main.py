import pygame
import random
import math
from pygame import mixer

# Initilize
pygame.init()
# Create Screen
screen = pygame.display.set_mode((1000, 800))
running = True
#background_sound
mixer.music.load('cosmic-drift-208809.mp3')
mixer.music.play(-1)
background = pygame.image.load('deep-space-planets-stars-science-fiction-wallpaper-beauty-deep-space.jpg')
pygame.display.set_caption('Space Defenders')
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

# player
playerimg = pygame.image.load('002-spaceship-1.png')
playerx = 500
playery = 540
playerx_change = 0

# Enemy
enemyimg = pygame.image.load('003-rocket.png')
enemyx = random.randint(0, 1000)
enemyy = random.randint(40, 150)
enemyx_change = 0.3
enemyy_change = 30

# laser
laserimg = pygame.image.load('laser.png')
laserx = 0
lasery = 570
laserx_change = 0
lasery_change = 1
laser_state = 'ready'

#score
score_value=0
font=pygame.font.Font('freesansbold.ttf',32)

textx=10
texty=10

#Game Over
over_font=pygame.font.Font('freesansbold.ttf',64)
def game_over_text():
    over_text=over_font.render('GAME OVER!',True,(255,255,255))
    screen.blit(over_text,(300,250))

def show_score(x,y):
    score=font.render('Score:'+str(score_value),True,(255,255,255))
    screen.blit(score,(x,y))
# Enemy
enemyImg = []
enemyx = []
enemyy = []
enemyx_change = []
enemyy_change = []
number_of_enemies = 6

for i in range(number_of_enemies):
    enemyImg.append(pygame.image.load('003-rocket.png'))
    enemyx.append(random.randint(0, 1000))
    enemyy.append(random.randint(40, 150))
    enemyx_change.append(0.3)
    enemyy_change.append(30)


def player(x, y):
    screen.blit(playerimg, (x, y))


def enemy(x, y):
    screen.blit(enemyimg, (x, y))


def fire_laser(x, y):
    global laser_state
    laser_state = 'fire'
    screen.blit(laserimg, (x + 13, y + 10))


def iscollision(enemyx, enemyy, laserx, lasery):
    distance = math.sqrt(math.pow((enemyx - laserx), 2) + math.pow((enemyy - lasery), 2))
    if distance < 27:
        return True
    else:
        return False


# Game loop
while running:

    for event in pygame.event.get():
        # if key stroke is pressed check weather chech right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerx_change = -0.9
            elif event.key == pygame.K_RIGHT:
                playerx_change = 0.9
            elif event.key == pygame.K_SPACE:
                if laser_state == 'ready':
                    laser_sound=mixer.Sound('laser-gun-81720.mp3')
                    laser_sound.play()
                    laserx = playerx
                    fire_laser(laserx, lasery)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerx_change = 0
        if event.type == pygame.QUIT:
            running = False
    # RGB-Red,Green,Blue
    screen.fill((0, 0, 0))
    # background Image
    screen.blit(background, (0, 0))
    playerx += playerx_change
    if playerx <= 0:
        playerx = 0
    elif playerx >= 936:
        playerx = 936
    # Enemy Movement
    for i in range(number_of_enemies):
        #Game Over
        if enemyy[i]>550:
            for j in range(number_of_enemies):
                enemyy[j]=2000
            game_over_text()
            break
        enemyx[i] += enemyx_change[i]
        if enemyx[i] <= 0:

            enemyx_change[i] = 0.3
            enemyy[i] += enemyy_change[i]
        elif enemyx[i] >= 936:

            enemyx_change[i] = -0.3
            enemyy[i] += enemyy_change[i]
            #collision
        collision = iscollision(enemyx[i], enemyy[i], laserx, lasery)
        if collision:
            explosion_sound=mixer.Sound('quot-dynamite-quot-sound-effect-205859.mp3')
            explosion_sound.play()
            lasery = 570
            laser_state = 'ready'
            score_value+=1
            enemyx[i] = random.randint(0, 935)
            enemyy[i] = random.randint(40, 150)
        enemy(enemyx[i],enemyy[i])
    # bullet movement
    if lasery <= 0:
        lasery = 570
        laser_state = 'ready'
    if laser_state == 'fire':
        fire_laser(laserx, lasery)
        lasery -= lasery_change

    player(playerx, playery)
    show_score(textx,texty)
    pygame.display.update()
