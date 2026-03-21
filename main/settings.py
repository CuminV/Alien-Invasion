import pygame

class Settings():
    """Class for a settings Alien Invasion game`s"""
    
    def __init__(self):
        #Screen settings
        self.screen_width = 1600
        self.screen_height = 800
        self.background = pygame.image.load('images/starsky.bmp')
        
        #Ship settings
        self.ship_speed = 2
        self.ship_limit = 3
        
        #Bullet settings
        self.bullet = pygame.image.load('images/bullet.bmp')
        self.bullet_speed = 3
        self.bullet_wigth = 50
        self.bullet_height = 50
        self.bullet_color = (235, 9, 9)
        self.bullets_allowed = 3
        
        #Alien settings
        self.alien_speed = 3
        self.fleet_drop_speed = 30
        self.fleet_direction = 1
        
        
        #sounds
        self.sound_explosion = pygame.mixer.Sound('sound/explosion.wav')
        self.sound_explosion.set_volume(0.5)
        
        self.sound_laser = pygame.mixer.Sound('sound/laser.wav')
        self.sound_laser.set_volume(0.5)