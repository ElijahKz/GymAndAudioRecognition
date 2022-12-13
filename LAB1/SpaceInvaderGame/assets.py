from appModules import pygame, os, random


WIDTH_SCREEN, HEIGHT_SCREEN = 750, 620

#Loading images
RED_SPACE_SHIP = pygame.transform.scale(pygame.image.load(os.path.join("assets", "pixel_ship_red_small.png")), (90, 90))
GREEN_SPACE_SHIP = pygame.transform.scale(pygame.image.load(os.path.join("assets", "pixel_ship_green_small.png")), (90, 90))
BLUE_SPACE_SHIP = pygame.transform.scale(pygame.image.load(os.path.join("assets", "pixel_ship_blue_small.png")), (90, 90))

#Player
YELLOW_SPACE_SHIP = pygame.transform.scale(pygame.image.load(os.path.join("assets", "pixel_ship_yellow_small.png")), (90, 90))

#Lasers
RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png")) 
YELLOW_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png")) 

#Background
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")), (WIDTH_SCREEN, HEIGHT_SCREEN))


