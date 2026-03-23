import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """Class for control bullet`s"""
    
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.image = pygame.image.load('images/bullet.bmp')
        
        self.rect = self.image.get_rect()
        self.rect.midtop = ai_game.ship.rect.midtop
        
        self.y = float(self.rect.y)
        
    def update(self):
        """Move bullet up to screen"""
        
        self.y -= self.settings.bullet_speed_factor
        self.rect.y = self.y
        
    def draw_bullet(self):
        """Draw bullet to screen"""
        self.screen.blit(self.image, self.rect)
        
    