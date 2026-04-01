import pygame
import pygame_menu

from alien_invasion import AlienInvasion
from config import Config

class AlienInvasionApp:

    def __init__(self):
        self.config = Config()
        self.screen = create_screen(self.config)
        self.current_state = 'menu'
        self.temp_settings = create_temp_settings(self.config)
        self.game = AlienInvasion(self.screen, self.config)
        self.menu = None
        self.setting_menu = None
        self.create_menus()
    
    
    def start_the_game(self):
        self.current_state = 'game'

    
    def create_menus(self):
        screen_width, screen_height = self.screen.get_size()
        self.menu = pygame_menu.Menu(
            "Alien Invasion",
            screen_width,
            screen_height,
            theme=pygame_menu.themes.THEME_DARK,
        )
        self.setting_menu = pygame_menu.Menu(
            'Settings',
            screen_width,
            screen_height,
            theme=pygame_menu.themes.THEME_DARK,
        )

        self.menu.add.button('PLAY', self.start_the_game)
        self.menu.add.button('SETTINGS', self.setting_menu)
        self.menu.add.button('EXIT', pygame_menu.events.EXIT)

        current_resolution_index = get_option_index(
            RESOLUTION_OPTIONS,
            self.config.resolution,
        )
        self.temp_settings['resolution'] = RESOLUTION_OPTIONS[current_resolution_index][1]
        if self.config.display_mode == 'fullscreen':
            self.setting_menu.add.label('Resolution: desktop only in fullscreen')
        else:
            self.setting_menu.add.selector(
                title='Resolution: ',
                items=RESOLUTION_OPTIONS,
                default=current_resolution_index,
                onchange=lambda _, val: self.temp_settings.update({'resolution': val}),
            )

        current_display_mode_index = get_option_index(
            DISPLAY_MODE_OPTIONS,
            self.config.display_mode,
        )
        self.temp_settings['display_mode'] = DISPLAY_MODE_OPTIONS[current_display_mode_index][1]
        self.setting_menu.add.selector(
            title='Display mode: ',
            items=DISPLAY_MODE_OPTIONS,
            default=current_display_mode_index,
            onchange=lambda _, val: self.temp_settings.update({'display_mode': val}),
        )

        self.setting_menu.add.range_slider(
            'Music: ',
            self.temp_settings['music_volume'],
            (0, 100),
            1,
            value_format=lambda x: str(int(x)),
            onchange=lambda val: self.temp_settings.update({'music_volume': val}),
        )
        self.setting_menu.add.range_slider(
            'SFX: ',
            self.config.sfx_volume,
            (0, 100),
            1,
            value_format=lambda x: str(int(x)),
            onchange=lambda val: self.temp_settings.update({'sfx_volume': val}),
        )

        current_difficulty_index = get_option_index(
            DIFFICULTY_OPTIONS,
            self.config.difficulty,
        )
        self.temp_settings['difficulty'] = DIFFICULTY_OPTIONS[current_difficulty_index][1]
        self.setting_menu.add.selector(
            title='Difficulty: ',
            items=DIFFICULTY_OPTIONS,
            default=current_difficulty_index,
            onchange=lambda _, val: self.temp_settings.update({'difficulty': val}),
        )

        self.setting_menu.add.button('Apply', self.apply_settings)
        self.setting_menu.add.button('Back', pygame_menu.events.BACK)


    def apply_settings(self):
        self.config.display_mode = self.temp_settings['display_mode']
        if self.config.display_mode != 'fullscreen':
            self.config.width, self.config.height = self.temp_settings['resolution']
        self.config.music_volume = self.temp_settings['music_volume']
        self.config.sfx_volume = self.temp_settings['sfx_volume']
        self.config.difficulty = self.temp_settings['difficulty']

        self.apply_video_settings()
        self.apply_audio_settings()
        self.game.settings.initialize_dynamic_settings()
        self.config.save()
        self.temp_settings = create_temp_settings(self.config)


    def apply_video_settings(self):
        self.screen = create_screen(self.config)
        self.game.screen = self.screen
        self.game.apply_new_resolution()
        self.create_menus()


    def apply_audio_settings(self):
        pygame.mixer.music.set_volume(self.config.music_volume / 100)
        self.game.settings.apply_config()


    def run(self):
        while True:
            events = pygame.event.get()
            
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
                    
            if self.current_state == 'menu':
                self.menu.update(events)
                self.menu.draw(self.screen)
            elif self.current_state == 'game':
                self.game.handle_events(events)
                self.game.update()
                self.game.draw()
            
            pygame.display.update()

RESOLUTION_OPTIONS = [
    ('1920x1080', (1920, 1080)),
    ('1600x900', (1600, 900)),
    ('1280x720', (1280, 720)),
]

DISPLAY_MODE_OPTIONS = [
    ('Fullscreen', 'fullscreen'),
    ('Windowed', 'windowed'),
    ('Borderless', 'borderless'),
]

DIFFICULTY_OPTIONS = [
    ('Easy', 'easy'),
    ('Medium', 'medium'),
    ('Hard', 'hard'),
]
    
pygame.init()

def create_screen(config):
    if config.display_mode == 'fullscreen':
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    elif config.display_mode == 'borderless':
        screen = pygame.display.set_mode(config.resolution, pygame.NOFRAME)
    else:
        screen = pygame.display.set_mode(config.resolution)

    config.width, config.height = screen.get_size()
    return screen


def get_option_index(options, value, fallback_index=0):
    for index, (_, option_value) in enumerate(options):
        if option_value == value:
            return index
    return fallback_index


def create_temp_settings(config):
    return {
        'resolution': config.resolution,
        'display_mode': config.display_mode,
        'music_volume': config.music_volume,
        'sfx_volume': config.sfx_volume,
        'difficulty': config.difficulty,
    }
    
    
def main():
    app = AlienInvasionApp()
    app.run()   
    
if __name__ == '__main__':
    main()



