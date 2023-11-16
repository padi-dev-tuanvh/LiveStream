import pygame
from Button import Button
from HostModel import HostModel
from ViewerHost import ViewerHost
import sys
import threading
from queue import Queue

# size of game
SCREEN_WIDTH = 1020
SCREEN_HEIGHT = 660

# get text font and size
def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font/fontText.ttf", size)

pygame.init()
default_left = False
default_right = False

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Livestream")

queue = Queue()
event_thread = threading.Event()

# set background image
BG = pygame.image.load("assets/img/background.png")

CENTER_SCREEN_WIDTH = SCREEN_WIDTH//2
CENTER_SCREEN_HEIGHT = SCREEN_HEIGHT//2
ONE_OVER_FOUR_SCREEN_WIDTH = CENTER_SCREEN_WIDTH//2
ONE_OVER_FOUR_SCREEN_HEIGHT = CENTER_SCREEN_HEIGHT//2


def Livestreaming():
    # set background
    SCREEN.blit(pygame.transform.scale(
       BG,SCREEN.get_size()), (0, 0))
    # set menu text
    # render: render the text into an image with a given color
    SETTINGS_TEXT =get_font(64).render(
        "Livestreaming", True, "#FFFFFF")
    SETTINGS_RECT = SETTINGS_TEXT.get_rect(
        center=(CENTER_SCREEN_WIDTH, ONE_OVER_FOUR_SCREEN_WIDTH))
    # set menu text to screen
    SCREEN.blit(SETTINGS_TEXT, SETTINGS_RECT)
    STOP_VIDEO = Button(image=pygame.transform.scale(pygame.image.load("assets/img/stop_video.png"), (60, 48)), pos=(CENTER_SCREEN_WIDTH, 3*ONE_OVER_FOUR_SCREEN_HEIGHT),
                         text_input="", font=get_font(16), base_color="#d7fcd4", hovering_color="White")

    while True:
        # get mouse position
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        for button in [STOP_VIDEO]:
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if STOP_VIDEO.checkForInput(MENU_MOUSE_POS):
                    print("Next Game")
        if not queue.empty():
            print(queue.get(timeout=1))
        pygame.display.update()

def watchingLivestream():
    # set background
    SCREEN.blit(pygame.transform.scale(
       BG,SCREEN.get_size()), (0, 0))
    # set menu text
    # render: render the text into an image with a given color
    SETTINGS_TEXT =get_font(64).render(
        "Watching livestream", True, "#FFFFFF")
    SETTINGS_RECT = SETTINGS_TEXT.get_rect(
        center=(CENTER_SCREEN_WIDTH, ONE_OVER_FOUR_SCREEN_WIDTH))
    # set menu text to screen
    SCREEN.blit(SETTINGS_TEXT, SETTINGS_RECT)
    CLOSE_WATCHING = Button(image=pygame.transform.scale(pygame.image.load("assets/img/close.png"), (60, 48)), pos=(CENTER_SCREEN_WIDTH, 3*ONE_OVER_FOUR_SCREEN_HEIGHT),
                         text_input="", font=get_font(16), base_color="#d7fcd4", hovering_color="White")

    while True:
        # get mouse position
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        for button in [CLOSE_WATCHING]:
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if CLOSE_WATCHING.checkForInput(MENU_MOUSE_POS):
                    print("Next Game")
                    event_thread.set()
                    mainGame()
        pygame.display.update()

def mainGame():
    # set background
    SCREEN.blit(pygame.transform.scale(
        BG, SCREEN.get_size()), (0, 0))
    # set menu text
    # render: render the text into an image with a given color
    SETTINGS_TEXT = get_font(64).render(
        "Livestream", True, "#FFFFFF")
    SETTINGS_RECT = SETTINGS_TEXT.get_rect(
        center=(CENTER_SCREEN_WIDTH, SCREEN_HEIGHT//5))
    # init button in menu

    FRAME_BUTTON = Button(image=pygame.transform.scale(pygame.image.load("assets/img/frame.png"), (450, 200)), pos=(CENTER_SCREEN_WIDTH, CENTER_SCREEN_HEIGHT),
                            text_input="", font=get_font(16), base_color="#d7fcd4", hovering_color="White")

    START_LIVE = Button(image=pygame.transform.scale(pygame.image.load("assets/img/Bar.png"), (280, 50)), pos=(CENTER_SCREEN_WIDTH, CENTER_SCREEN_HEIGHT-75),
                            text_input="Bắt đầu", font=get_font(36), base_color="#d7fcd4", hovering_color="Black")
    WATCH_LIVE = Button(image=pygame.transform.scale(pygame.image.load("assets/img/Bar.png"), (280, 50)), pos=(CENTER_SCREEN_WIDTH, CENTER_SCREEN_HEIGHT-25),
                            text_input="Xem livestream", font=get_font(36), base_color="#d7fcd4", hovering_color="Black")
    ABOUT_BUTTON = Button(image=pygame.transform.scale(pygame.image.load("assets/img/Bar.png"), (280, 50)), pos=(CENTER_SCREEN_WIDTH, CENTER_SCREEN_HEIGHT+25),
                            text_input="Giới thiệu", font=get_font(36), base_color="#d7fcd4", hovering_color="Black")
    QUIT_BUTTON = Button(image=pygame.transform.scale(pygame.image.load("assets/img/Bar.png"), (280, 50)), pos=(CENTER_SCREEN_WIDTH, CENTER_SCREEN_HEIGHT+75),
                            text_input="Thoát", font=get_font(36), base_color="#d7fcd4", hovering_color="Black")

    # set menu text to screen
    SCREEN.blit(SETTINGS_TEXT, SETTINGS_RECT)

    while True:
        # get mouse position
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        # set button to screen
        for button in [FRAME_BUTTON, START_LIVE, WATCH_LIVE, QUIT_BUTTON, ABOUT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        # check for event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if START_LIVE.checkForInput(MENU_MOUSE_POS):
                    print("Start livestream")
                    host = HostModel()
                    host.connectServer()
                    inp = threading.Thread(target = host.inputs)
                    inp.start()
                    out = threading.Thread(target=host.output,args=(queue,))
                    out.daemon = True
                    out.start()
                    Livestreaming()
                    break
                if WATCH_LIVE.checkForInput(MENU_MOUSE_POS):
                    print("Watch livestream")
                    viewer = ViewerHost(event_thread)
                    viewer.connectServer()
                    out = threading.Thread(target = viewer.output)
                    out.start()
                    watchingLivestream()
                    break
                if ABOUT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    print("About us")
                    
                    break
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    print("Exit Game")
                    pygame.quit()
                    sys.exit()
        pygame.display.update()

mainGame()


