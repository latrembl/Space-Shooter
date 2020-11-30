# Lucas Tremblay
# very simple space shooter game, controlled on the x-axis by your mouse
# destroy asteroids before they reach the planet
# to win you must survive the entire time without your ship or planet exploding!

import pygame
import random
from pathlib import Path

# ----------------------------------------------------------------------------------------------------------------------

# global color definitions 
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (124, 252, 0)

# difficulty - global asteroid count (more asteroids = greater difficulty)
debugEasy = 3
debugImpossible = 2000
easy = 400
normal = 600
hard = 900
asteroidCount = normal


# ----------------------------------------------------------------------------------------------------------------------


# planet class
class Planet(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # store absolute path in filename
        filename = Path("planet_img.jpg").absolute()
        # load filename as str(important) and convert image to be used for the planet
        self.image = pygame.image.load(str(filename)).convert()
        self.rect = self.image.get_rect()


# explosion class
class Explosion(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # store absolute path in filename
        filename = Path("explosion_img.jpg").absolute()
        # load filename as str(important) and convert image to be used for the planet
        self.image = pygame.image.load(str(filename)).convert()
        self.rect = self.image.get_rect()


# asteroid class
class Asteroid(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # store absolute path in filename
        filename = Path("asteroid_img.jpg").absolute()
        # load filename as str(important) and convert image to be used for the planet
        self.image = pygame.image.load(str(filename)).convert()
        self.rect = self.image.get_rect()


# player class
class Player(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # store absolute path in filename
        filename = Path("ship_img.jpg").absolute()
        # load filename as str(important) and convert image to be used for the planet
        self.image = pygame.image.load(str(filename)).convert()
        self.rect = self.image.get_rect()


# laser class
class Laser(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # height width and color of laser surface
        self.image = pygame.Surface([5, 10])
        self.image.fill(blue)
        self.rect = self.image.get_rect()


# function to play music in background, infinite loop
def music():
    filename = Path("music.xm").absolute()
    # load filename as str(important)
    pygame.mixer.music.load(str(filename))
    pygame.mixer.music.play(-1, 0)


# function to place asteroids
def asteroid():
    for i in range(asteroidCount):
        # This represents an asteroid
        asteroid_obj = Asteroid()

        # Set a random location for the asteroid
        asteroid_obj.rect.x = random.randrange(-500, 500)
        asteroid_obj.rect.y = random.randrange(-3000, -19)

        # Add the asteroid to the list of objects)
        asteroidList.add(asteroid_obj)
        allSpritesList.add(asteroid_obj)


# ----------------------------------------------------------------------------------------------------------------------

# Initialize Pygame
pygame.init()

# define the screen
size = [500, 700]
screen = pygame.display.set_mode(size)

# window title and icon
pygame.display.set_caption('Space Shooter')
filename = Path("ship_img.jpg").absolute()
# load filename as str(important)
icon = pygame.image.load(str(filename))
pygame.display.set_icon(icon)

# hide mouse cursor
pygame.mouse.set_visible(False)

pygame.event.set_grab(True)

# main function calls below
allSpritesList = pygame.sprite.RenderPlain()
asteroidList = pygame.sprite.RenderPlain()
laserList = pygame.sprite.RenderPlain()
music()
asteroid()
planet = Planet()
explosion = Explosion()

# coordinates for planet/player/explosion
planet.rect.y = 650
planet.rect.x = 0
player = Player()
player.rect.y = 600
explosion.rect.y = 400
explosion.rect.x = -100

# game counters
score = 0
shipHealth = 100
timeSinceStart = 60
planetHealth = 200

# sprite list
allSpritesList.add(player)
allSpritesList.add(planet)

# how fast screen updates
clock = pygame.time.Clock()

# set game loop to RUNNING
RUNNING = True

# main game loop, plays while RUNNING is True
while RUNNING:

    # when the pygame.QUIT is called, end the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False
        # when the escape button is pressed, quit the game
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                RUNNING = False

        # laser animation
        if event.type == pygame.MOUSEBUTTONDOWN:
            # play laser sound when left mouse button is clocked
            laser1 = Laser()
            laser2 = Laser()
            filename = Path("laser_sound.wav").absolute()
            # load filename as str(important)
            sound1 = pygame.mixer.Sound(str(filename))
            sound1.set_volume(.1)
            sound1.play()
            # set initial laser position equal to the player position
            laser1.rect.x = player.rect.x
            laser2.rect.x = player.rect.x + 15
            laser1.rect.y = laser2.rect.y = player.rect.y
            # add laser to sprite and laser lists
            allSpritesList.add(laser1)
            allSpritesList.add(laser2)
            laserList.add(laser1)
            laserList.add(laser2)

    # increase time since start
    timeSinceStart -= .05

    # if enough time has passed, player wins the game
    if timeSinceStart <= 0:
        pygame.time.wait(500)
        font = pygame.font.SysFont("Agency FB", 30)
        defendedText = font.render("YOU DEFENDED YOUR PLANET!", True, green)
        screen.blit(defendedText, (100, 260))
        pygame.display.flip()
        pygame.time.wait(4000)
        RUNNING = False

    # quit font
    font = pygame.font.SysFont("Agency FB", 15)
    quitText1 = "ESC to Quit"
    quitText2 = font.render(quitText1, True, red)
    screen.blit(quitText2, (5, 5))

    # score font
    font = pygame.font.SysFont("Agency FB", 25)
    scoreText1 = "Score: " + str(score)
    scoreText2 = font.render(scoreText1, True, black)
    screen.blit(scoreText2, (20, 660))

    # ship health font
    font = pygame.font.SysFont("Agency FB", 25)
    shipText1 = "Ship Health: " + str(shipHealth)
    shipText2 = font.render(shipText1, True, black)
    screen.blit(shipText2, (360, 660))

    # planet health font
    font = pygame.font.SysFont("Agency FB", 17)
    planetText1 = "Planet Health: " + str(planetHealth)
    planetText2 = font.render(planetText1, True, black)
    screen.blit(planetText2, (195, 675))

    # time left font
    font = pygame.font.SysFont("Agency FB", 15)
    timeText1 = "Time Left: " + str('%.2f' % timeSinceStart)
    timeText2 = font.render(timeText1, True, black)
    screen.blit(timeText2, (205, 660))
    pygame.display.flip()

    # collision detection
    collide = pygame.sprite.spritecollide(player, asteroidList, True)
    collidePlanet = pygame.sprite.spritecollide(planet, asteroidList, True)

    # if collision is detected between player and asteroid, remove the asteroid and deduct a life
    if collide:
        filename = Path("hit_sound.wav").absolute()
        # load filename as str(important)
        sound2 = pygame.mixer.Sound(str(filename))
        sound2.set_volume(.2)
        sound2.play()
        shipHealth -= 20

    # if collision is detected between planet and asteroid, remove the asteroid and deduct 5 health from the planet
    if collidePlanet:
        planetHealth -= 2

    # if lives is less than zero, end game and display game over
    if shipHealth <= 0 or planetHealth <= 0:
        pygame.time.wait(500)
        filename = Path("explosion_sound.wav").absolute()
        # load filename as str(important)
        sound3 = pygame.mixer.Sound(str(filename))
        sound3.set_volume(.5)
        sound3.play()
        # when game ends, remove sprites from list
        allSpritesList.add(explosion)
        allSpritesList.remove(planet)
        allSpritesList.remove(player)
        allSpritesList.remove(asteroid)
        allSpritesList.draw(screen)
        font = pygame.font.SysFont("Agency FB", 30)
        if shipHealth <= 0:
            loseText = font.render("YOUR SHIP WAS DESTROYED", True, red)
            screen.blit(loseText, (120, 260))
        elif planetHealth <= 0:
            loseText = font.render("YOUR PLANET WAS DESTROYED", True, red)
            screen.blit(loseText, (110, 260))
        pygame.display.flip()
        # pause before closing the game
        pygame.time.wait(8000)
        RUNNING = False

    # mechanics for each laser
    for laser in laserList:

        # laser up 5 pixels
        laser.rect.y -= 15

        # detect whether laser hits an asteroid, remove asteroid
        asteroid_hit_list = pygame.sprite.spritecollide(laser, asteroidList, True)

        # for each hit, remove laser and add 1 to the score
        for asteroid in asteroid_hit_list:
            laserList.remove(laser)
            allSpritesList.remove(laser)
            score += 1

        # remove the laser if it goes off screen
        if laser.rect.y < -10:
            laserList.remove(laser)
            allSpritesList.remove(laser)

    # animation for moving asteroids toward bottom of screen
    for asteroid in asteroidList:
        asteroid.rect.y += 3

    # get the mouse position
    pos = pygame.mouse.get_pos()
    # set player x to mouse position
    player.rect.x = pos[0]
    # set screen color
    screen.fill(black)
    # draw all sprites in all sprites list
    allSpritesList.draw(screen)
    # set frames per second
    clock.tick(20)

pygame.quit()
