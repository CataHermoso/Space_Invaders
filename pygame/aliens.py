from turtle import Screen
import pygame

class Alien(pygame.sprite.Sprite):
    def __init__(self,color,x,y):
        super().__init__()
        file_path = '//Users/catalinahermoso/Desktop/pygame/graphics/' + color + '.png'
        self.image = pygame.image.load(file_path).convert_alpha()
        self.rect = self.image.get_rect(topleft = (x,y))

        #setup for score
        if color == 'blue':
            self.value = 100
        elif color == 'green':
            self.value = 200
        elif color == 'pink':
            self.value = 250
        else:
            self.value = 400

    def update(self,direction):
        self.rect.x += direction

class Boss(pygame.sprite.Sprite):
    def __init__(self,side, screen_width):
        super().__init__()
        self.image = pygame.image.load('//Users/catalinahermoso/Desktop/pygame/graphics/red.png').convert_alpha()
        
        if side == 'right':
            x = screen_width + 50
            self.speed = -3
        else:
            x = -50
            self.speed = 3
        
        self.rect = self.image.get_rect(topleft = (x,20))

    def update(self):
        self.rect.x += self.speed