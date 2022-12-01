from interfaces.Abstract import AbstractEntityGame
from assets import RED_SPACE_SHIP, RED_LASER
from assets import GREEN_SPACE_SHIP,GREEN_LASER
from assets import BLUE_SPACE_SHIP, BLUE_LASER
from appModules import pygame
from Model.laser import Laser

class Enemy(AbstractEntityGame):    
    def __init__(self, x , y ,color, health=100):
        super().__init__(x,y,health)
        self.COLOR_MAP = {
            "red":(RED_SPACE_SHIP, RED_LASER),
            "green":(GREEN_SPACE_SHIP, GREEN_LASER),
            "blue":(BLUE_SPACE_SHIP, BLUE_LASER)
        }
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)
    def move(self, vel):
        self.y += vel
    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x - 10 , self.y , self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1