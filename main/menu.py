import pygame
import pygame_menu
from alien_invasion import AlienInvasion

pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

current_state = "menu"
game = AlienInvasion(screen)


def start_the_game():
    global current_state
    current_state = "game"


menu = pygame_menu.Menu(
    "Alien Invasion", 1920, 1080, 
    theme=pygame_menu.themes.THEME_DARK
)

menu.add.button('PLAY', start_the_game)
menu.add.button('EXIT', pygame_menu.events.EXIT)


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


    

    


    






    