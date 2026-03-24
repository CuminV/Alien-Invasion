import pygame

class Settings():
    """Class for a settings Alien Invasion game`s"""
    
    def __init__(self):
        #Static settings
        #Screen settings
        self.screen_width = 1600
        self.screen_height = 800
        self.background = pygame.image.load('images/starsky.bmp')
        
        #Ship settings
        self.ship_limit = 3
        
        #Bullet settings
        self.bullet = pygame.image.load('images/bullet.bmp')
        self.bullet_wigth = 50
        self.bullet_height = 50
        self.bullets_allowed = 3
        
        #Alien settings
        self.fleet_drop_speed = 5
        
        
        #sounds
        self.sound_explosion = pygame.mixer.Sound('sound/explosion.wav')
        self.sound_explosion.set_volume(0.5)
        
        self.sound_laser = pygame.mixer.Sound('sound/laser.wav')
        self.sound_laser.set_volume(0.5)
        
        
        #Dynamic settings
        
        self.speedup_scale = 1.1
        self.score_scale = 1.5
        
        self.initialize_dynamic_settings()
        
        
        
        
    
    def initialize_dynamic_settings(self):
        
        #Ship settings
        self.ship_speed_factor = 1.5
        
        #Bullet settings
        self.bullet_speed_factor = 3.0
        
        #Alien settings
        self.alien_speed_factor = 1.0
        self.fleet_direction = 1
        
        #Score
        self.alien_points = 50
        
        
    def increase_speed(self):
        self.alien_points = int(self.alien_points * self.score_scale)   
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale