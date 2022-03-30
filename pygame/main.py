import pygame, sys
from player import Player
import obstacle
from aliens import Alien, Boss
from random import choice, randint
from laser import Laser

#change the logo of the game!!!!!

class Game:
    def __init__(self): #usual initiate method of a class (player, obstacles, aliens)
        #player setup
        player_sprite = Player((screen_width/2,screen_height),screen_width,5)
        self.player = pygame.sprite.GroupSingle(player_sprite)

        #health and score setup
        self.lives = 3
        self.lives_surf = pygame.image.load('/Users/catalinahermoso/Desktop/pygame/graphics/heart.png').convert_alpha()
        self.live_x_start_pos = screen_width - (self.lives_surf.get_size()[0] * 2 + 20)
        self.score = 0
        self.font = pygame.font.Font('/Users/catalinahermoso/Desktop/pygame/slkscre.ttf', 20)

        #obstacle setup (attributes)
        self.shape = obstacle.shape
        self.block_size = 6
        self.blocks = pygame.sprite.Group()
        self.obstacle_amount = 4 #how many obstacles we want
        self.obstacle_x_positions = [num * (screen_width/self.obstacle_amount) for num in range(self.obstacle_amount)] #space out the obstacles on the screem
        self.create_multiple_obstacles(*self.obstacle_x_positions,x_start=screen_width/15,y_start=450)

        #alien setup
        self.aliens = pygame.sprite.Group()
        self.alien_lasers = pygame.sprite.Group()
        self.alien_setup(rows=6, cols=8)
        self.alien_direction = 1

        #boss setup
        self.boss = pygame.sprite.GroupSingle()
        self.boss_spawn_time = randint(40,80) #everytime we run the run method we substract a certain amount from here and whenever it get 0 we spawn another alien


    def create_obstacle(self,x_start,y_start,offset_x):
        for row_index,row in enumerate(self.shape): #we go through every row in shape, and enumerate fucnt enumerates each row so we know in which row we are on
            for col_index, col in enumerate(row): #gives each column from every row an index (0,0)
                if col == 'x':
                    x = x_start + col_index * self.block_size + offset_x 
                    #(x_start)=how far we are from the left
                    #(col_index * self.block_size)=to check what position we are on inside of the shape
                    #(offset_x)=if we create multiple obstacles this will make that not all of them are not in the same position. the fisrt one is in pos 0, te second 100, the third 200 (has its shown in the #obstacle setup in self.create_miltiple_obstacles)
                    y = y_start + row_index * self.block_size
                    block = obstacle.Block(self.block_size,(129,136,192),x,y)
                    self.blocks.add(block)

    def create_multiple_obstacles(self,*offset,x_start,y_start):
        for offset_x in offset:
            self.create_obstacle(x_start,y_start,offset_x)

    def alien_setup(self,rows,cols,x_distance=60,y_distance=48,x_offset=60,y_offset=79):
        for row_index,row in enumerate(range(rows)):
            for col_index, col in enumerate(range(cols)):
                x = col_index * x_distance + x_offset
                y = row_index * y_distance + y_offset

                #color of the aliens depending on the row they are in
                if row_index == 0:
                    alien_sprite = Alien('pink',x,y)
                elif 1<= row_index <= 2:
                    alien_sprite = Alien('green',x,y)
                else:
                    alien_sprite = Alien('blue',x,y)
                self.aliens.add(alien_sprite)

    def alien_position_checker(self):
        all_aliens = self.aliens.sprites()
        for alien in all_aliens:
            if alien.rect.right >= screen_width:
                self.alien_direction = -1
                self.alien_move_down(2)
            if alien.rect.left <= 0:
                self.alien_direction = 1
                self.alien_move_down(2)

    def alien_move_down(self,distance):
        if self.aliens:
            for alien in self.aliens.sprites():
                alien.rect.y += distance
    
    def alien_shoot(self):
        if self.aliens.sprites():
            random_alien = choice(self.aliens.sprites())
            laser_sprite = Laser(random_alien.rect.center,6,screen_height)
            self.alien_lasers.add(laser_sprite)

    def boss_alien_timer(self): #we start with the randint fomr boss setup, and we reduce it by one, every time until we get 0, after that we run the statment of self.extra.add and we add a new alien
        self.boss_spawn_time -= 1
        if self.boss_spawn_time <= 0:
            self.boss.add(Boss(choice(['right','left']),screen_width))
            self.boss_spawn_time = randint(400,800) #the next extra alien is gonna be a little bit faster

    def collision_check(self):

        #player lasers
        if self.player.sprite.lasers:
            for laser in self.player.sprite.lasers:
                #obstacle collisions
                if pygame.sprite.spritecollide(laser,self.blocks,True): #we destroy the block as soon as it collides with the laser
                    laser.kill() #the laser stops when it collides with the obstacle
                    
                #alien collisions
                aliens_hit = pygame.sprite.spritecollide(laser,self.aliens,True)
                if aliens_hit:
                    for alien in aliens_hit:
                        self.score += alien.value
                    laser.kill()
                    

                #boss collision
                if pygame.sprite.spritecollide(laser,self.boss,True): #we destroy the block as soon as it collides with the laser
                    self.score += 500
                    laser.kill()
                    
        #alien lasers
        if self.alien_lasers:
            for laser in self.alien_lasers:
                
                #obstacle collision
                if pygame.sprite.spritecollide(laser,self.blocks,True):
                    laser.kill()
                
                #player collision
                if pygame.sprite.spritecollide(laser,self.player,False): #false so we do not destroy the player
                    laser.kill()
                    self.lives -= 1
                    if self.lives <= 0:
                        pygame.quit()
                        sys.exit()

        #aliens
        if self.aliens: #check if there are any aliens
            for alien in self.aliens:
                pygame.sprite.spritecollide(alien,self.blocks,True)

                if pygame.sprite.spritecollide(alien,self.player,False):
                    pygame.quit()
                    sys.exit()
 
    def display_lives(self):
        for live in range(self.lives):
            x = self.live_x_start_pos + (live * self.lives_surf.get_size()[0] - 7)# we dont want to place all the lives there
            screen.blit(self.lives_surf,(x,8))

    def display_score(self):
        score_surf = self.font.render(f'score: {self.score}',False,'white') #score surface
        score_rect = score_surf.get_rect(topleft = (10,7)) #rect on the surf
        screen.blit(score_surf,score_rect) #display it on the screen

    def victory_message(self):
        if not self.aliens.sprites():
            #f not self.boss.GroupSingle():
                victory_surf = self.font.render('You Won!', False, 'white')
                victory_rect = victory_surf.get_rect(center = (screen_width / 2, screen_width / 2))
                screen.blit(victory_surf, victory_rect)

    def run(self): 
        #update all sprite groups
        self.player.update()
        self.alien_lasers.update()
        self.boss.update()
        #extra updates
        self.aliens.update(self.alien_direction)
        self.alien_position_checker()
        self.boss_alien_timer()
        self.collision_check()

        #draw all
        self.player.sprite.lasers.draw(screen)
        self.player.draw(screen) #draw the player on our display surface
        self.blocks.draw(screen)
        self.aliens.draw(screen)
        self.alien_lasers.draw(screen)
        self.boss.draw(screen)
        self.display_lives()
        self.display_score()
        self.victory_message()

if __name__ == '__main__':
    pygame.init()
    screen_width = 600
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    game = Game()

    ALIENLASER = pygame.USEREVENT + 1
    pygame.time.set_timer(ALIENLASER,800)

    pygame.display.set_caption('Space Invaders')

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == ALIENLASER:
                game.alien_shoot()

        screen.fill((30,30,30))
        game.run() #runs the def run from above 

        pygame.display.flip()
        clock.tick(60)