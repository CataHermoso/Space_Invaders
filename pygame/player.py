import pygame
from laser import Laser

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, constraint, speed):
        super().__init__()
        self.image = pygame.image.load('/Users/catalinahermoso/Desktop/pygame/graphics/player.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom = pos)
        self.speed = speed
        self.max_x_constraint = constraint
        self.ready = True
        self.laser_time = 0
        self.laser_cooldown = 600 #we are only gonna be able to shoot the laser every 600 mseconds

        self.lasers = pygame.sprite.Group()

    def get_input(self): #movement of player
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        elif keys[pygame.K_LEFT]:
            self.rect.x -= self.speed

        if keys[pygame.K_SPACE] and self.ready: #we can only shoot pessing SPACE and if the cooldown is done
            self.shoot_laser()
            self.ready = False #everytime we shoot it changes to false to start the cooldown
            self.laser_time = pygame.time.get_ticks() #timer ; we use it once

    def recharge(self):
        if not self.ready:
            current_time = pygame.time.get_ticks() #loop of the one above
            if current_time - self.laser_time >= self.laser_cooldown: #we check the amount of time we've been playing since the last shot, and the we substract the starting time (or the last time we shot), if it's 600 we can shoot again!
                self.ready = True
            
    def constraint(self): #so the player stays on the screen
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= self.max_x_constraint:
            self.rect.right = self.max_x_constraint

    def shoot_laser(self): #it needs a timer so the player does not keep shooting forever, the game would be very simple if so
       self.lasers.add(Laser(self.rect.center, -8, self.rect.bottom))

    def update(self): #making every funct work
        self.get_input()
        self.constraint()
        self.recharge()
        self.lasers.update()