import pygame
import pygame_menu

from alien_invasion import AlienInvasion
from config import Config


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
config = Config()


def create_screen():
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


screen = create_screen()
current_state = "menu"

temp_settings = {
    'resolution': config.resolution,
    'display_mode': config.display_mode,
    'music_volume': config.music_volume,
    'sfx_volume': config.sfx_volume,
    'difficulty': config.difficulty,
}

game = AlienInvasion(screen, config)


def start_the_game():
    global current_state
    current_state = "game"


def create_menus():
    global menu, setting_menu

    screen_width, screen_height = screen.get_size()
    menu = pygame_menu.Menu(
        "Alien Invasion",
        screen_width,
        screen_height,
        theme=pygame_menu.themes.THEME_DARK,
    )
    setting_menu = pygame_menu.Menu(
        'Settings',
        screen_width,
        screen_height,
        theme=pygame_menu.themes.THEME_DARK,
    )

    menu.add.button('PLAY', start_the_game)
    menu.add.button('SETTINGS', setting_menu)
    menu.add.button('EXIT', pygame_menu.events.EXIT)

    current_resolution_index = get_option_index(
        RESOLUTION_OPTIONS,
        config.resolution,
    )
    temp_settings['resolution'] = RESOLUTION_OPTIONS[current_resolution_index][1]
    if config.display_mode == 'fullscreen':
        setting_menu.add.label('Resolution: desktop only in fullscreen')
    else:
        setting_menu.add.selector(
            title='Resolution: ',
            items=RESOLUTION_OPTIONS,
            default=current_resolution_index,
            onchange=lambda _, val: temp_settings.update({'resolution': val}),
        )

    current_display_mode_index = get_option_index(
        DISPLAY_MODE_OPTIONS,
        config.display_mode,
    )
    temp_settings['display_mode'] = DISPLAY_MODE_OPTIONS[current_display_mode_index][1]
    setting_menu.add.selector(
        title='Display mode: ',
        items=DISPLAY_MODE_OPTIONS,
        default=current_display_mode_index,
        onchange=lambda _, val: temp_settings.update({'display_mode': val}),
    )

    setting_menu.add.range_slider(
        'Music: ',
        config.music_volume,
        (0, 100),
        1,
        value_format=lambda x: str(int(x)),
        onchange=lambda val: temp_settings.update({'music_volume': val}),
    )
    setting_menu.add.range_slider(
        'SFX: ',
        config.sfx_volume,
        (0, 100),
        1,
        value_format=lambda x: str(int(x)),
        onchange=lambda val: temp_settings.update({'sfx_volume': val}),
    )

    current_difficulty_index = get_option_index(
        DIFFICULTY_OPTIONS,
        config.difficulty,
    )
    temp_settings['difficulty'] = DIFFICULTY_OPTIONS[current_difficulty_index][1]
    setting_menu.add.selector(
        title='Difficulty: ',
        items=DIFFICULTY_OPTIONS,
        default=current_difficulty_index,
        onchange=lambda _, val: temp_settings.update({'difficulty': val}),
    )

    setting_menu.add.button('Apply', apply_settings)
    setting_menu.add.button('Back', pygame_menu.events.BACK)


def apply_video_settings():
    global screen

    screen = create_screen()
    game.screen = screen
    game.apply_new_resolution()
    create_menus()


def apply_audio_settings():
    pygame.mixer.music.set_volume(config.music_volume / 100)
    game.settings.apply_config()


def apply_settings():
    config.display_mode = temp_settings['display_mode']
    if config.display_mode != 'fullscreen':
        config.width, config.height = temp_settings['resolution']
    config.music_volume = temp_settings['music_volume']
    config.sfx_volume = temp_settings['sfx_volume']
    config.difficulty = temp_settings['difficulty']

    apply_video_settings()
    apply_audio_settings()
    game.settings.initialize_dynamic_settings()
    config.save()


create_menus()
while True:
    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            exit()

    if current_state == "menu":
        menu.update(events)
        menu.draw(screen)
    elif current_state == "game":
        game.handle_events(events)
        game.update()
        game.draw()

    pygame.display.update()
