from interfaces.Abstract import AbstractEntityGame 
#from interfaces.colision import CollisionInteraction
from assets import YELLOW_LASER, YELLOW_SPACE_SHIP
from appModules import pygame
from assets import WIDTH_SCREEN, HEIGHT_SCREEN

class Player(AbstractEntityGame):
    def __init__(self, x, y, health=100):
        super().__init__(x, y )
        self.ship_img = YELLOW_SPACE_SHIP
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health
    
    def move_lasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT_SCREEN):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)    

    def healthbar(self, window):
        pygame.draw.rect(window, (255,0,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0,255,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health/self.max_health) , 10))

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)
    
