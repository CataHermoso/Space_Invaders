import pygame

class Block(pygame.sprite.Sprite):
    def __init__(self,size,color,x,y):
        super().__init__()
        self.image = pygame.Surface((size,size)) #they are sqares thats why both arguments are the same
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft = (x,y))

shape = [
'  xxxxx  ',
' xxxxxxx ',
'xxxxxxxxx',
'xxxxxxxxx',
'xx     xx',
'x       x',
] 
#we either have a '' or an 'x'; whenever we have an x we are gonna create a Block; if there's a space there isnt going to be a Block