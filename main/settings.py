import pygame

class Settings:
    """Runtime game settings and loaded resources."""

    def __init__(self, config):
        self.config = config

        # Screen settings
        self.screen_width = config.width
        self.screen_height = config.height
        self.display_mode = config.display_mode
        self._background_source = pygame.image.load('images/starsky.bmp')
        self.background = pygame.transform.scale(
            self._background_source,
            (self.screen_width, self.screen_height),
        )

        # Ship settings
        self.ship_limit = 3

        # Bullet settings
        self.bullet_wigth = 50
        self.bullet_height = 50
        self.bullets_allowed = 3

        # Alien settings
        self.fleet_drop_speed = 5

        # Sounds
        self.sound_explosion = pygame.mixer.Sound('sound/explosion.wav')
        self.sound_laser = pygame.mixer.Sound('sound/laser.wav')

        # Dynamic settings
        self.speedup_scale = 1.1
        self.score_scale = 1.5

        self.apply_config()
        self.initialize_dynamic_settings()

    def apply_config(self):
        self.screen_width = self.config.width
        self.screen_height = self.config.height
        self.display_mode = self.config.display_mode
        self.background = pygame.transform.scale(
            self._background_source,
            (self.screen_width, self.screen_height),
        )

        normalized_sfx_volume = self.config.sfx_volume / 100
        self.sound_laser.set_volume(normalized_sfx_volume)
        self.sound_explosion.set_volume(normalized_sfx_volume)

    def initialize_dynamic_settings(self):
        difficulty_presets = {
            'easy': (1.5, 1.0, 3.0),
            'medium': (2.5, 2.0, 5.0),
            'hard': (3.5, 3.0, 7.0),
        }
        ship_speed, alien_speed, bullet_speed = difficulty_presets.get(
            self.config.difficulty,
            difficulty_presets['medium'],
        )

        # Ship settings
        self.ship_speed_factor = ship_speed

        # Bullet settings
        self.bullet_speed_factor = bullet_speed

        # Alien settings
        self.alien_speed_factor = alien_speed
        self.fleet_direction = 1

        # Score
        self.alien_points = 50

    def increase_speed(self):
        self.alien_points = int(self.alien_points * self.score_scale)
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
