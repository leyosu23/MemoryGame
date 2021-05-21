import pygame
from random import *

# setup the game level
def setup(level):
    # how long able to remember before the game starts
    global display_time
    display_time = 5 - (level // 3)
    display_time = max(display_time, 1) # if less than 1 then set 1

    # how many numbers has to be shown
    number_count = (level // 3) + 5
    number_count = min(number_count, 20) # if number is more than 20 then set 20

    # randomly deploy numbers
    shuffle_grid(number_count)

# shuffle numbers (core algorithm)
def shuffle_grid(number_count):
    rows = 5
    columns = 9

    cell_size = 130
    button_size = 110
    screen_left_margin = 55
    screen_top_margin = 20

    # [[0, 0, 0, 0, 0, 0, 0, 5, 0],
    #  [0, 0, 0, 0, 0, 4, 0, 0, 0],
    #  [0, 0, 1, 0, 0, 0, 2, 0, 0],
    #  [0, 0, 0, 0, 3, 0, 0, 0, 0],
    #  [0, 0, 0, 0, 0, 0, 0, 0, 0]]
    grid = [[0 for col in range(columns)] for row in range(rows)] # 5 x 9

    number = 1 # number 1 to n
    while number <= number_count:
        row_idx = randrange(0, rows) # randomly select 0, 1, 2, 3, 4
        col_idx = randrange(0, columns) # randomly select 0 ~ 8

        if grid[row_idx][col_idx] == 0:
            grid[row_idx][col_idx] = number
            number += 1

            # decide x,y coordinates
            center_x = screen_left_margin + (col_idx * cell_size) + (cell_size / 2)
            center_y = screen_top_margin + (row_idx * cell_size) + (cell_size / 2)

            # make the number buttons
            button = pygame.Rect(0, 0, button_size, button_size)
            button.center = (center_x, center_y)

            number_buttons.append(button)



def display_start_screen():
    pygame.draw.circle(screen, WHITE, start_button.center, 60, 5)

    msg = game_font.render(f"{curr_level}", True, WHITE)
    msg_rect = msg.get_rect(center=start_button.center)
    screen.blit(msg, msg_rect)

def display_game_screen():
    global hidden

    if not hidden:
        elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000 # ms -> sec
        if elapsed_time > display_time:
            hidden = True

    for idx, rect in enumerate(number_buttons, start=1):
        if hidden: # hide the button
            # draw button rect
            pygame.draw.rect(screen, WHITE, rect)
        else:
            # number text
            cell_text = game_font.render(str(idx), True, WHITE)
            text_rect = cell_text.get_rect(center=rect.center)
            screen.blit(cell_text, text_rect)


# check pos
def check_buttons(pos):
    global start, start_ticks

    if start:
        check_number_buttons(pos)
    elif start_button.collidepoint(pos):
        start = True
        start_ticks = pygame.time.get_ticks()

def check_number_buttons(pos):
    global start, hidden, curr_level

    for button in number_buttons:
        if button.collidepoint(pos):
            if button == number_buttons[0]:
                del number_buttons[0]        
                if not hidden:
                    hidden = True
            else:
                game_over()
            break

    # in case players find all the buttons correct
    if len(number_buttons) == 0:
        start = False
        hidden = False
        curr_level += 1
        setup(curr_level)

def game_over():
    global running
    running = False
    
    msg = game_font.render(f"Your level is {curr_level}", True, WHITE)
    msg_rect = msg.get_rect(center=(screen_width/2, screen_height/2))

    screen.fill(BLACK)
    screen.blit(msg, msg_rect)

# initialize
pygame.init()
pygame.font.init()
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Memory Game")
game_font = pygame.font.SysFont("arialrounded", 100)

# start button
start_button = pygame.Rect(0, 0, 120, 120)
start_button.center = (120, screen_height - 120)

# colors
BLACK = (0, 0, 0) # RGB 
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)

number_buttons = []
curr_level = 1
display_time = None
start_ticks = None

# game has started or not?
start = False
# the number button is hidden or not?
hidden = False

# setup the level
setup(curr_level)

# game loop
running = True
while running:
    click_pos = None

    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONUP:
            click_pos = pygame.mouse.get_pos()

    # fill the screen with black
    screen.fill(BLACK)

    if start: 
        display_game_screen()
    else:        
        display_start_screen()

    if click_pos:
        check_buttons(click_pos)

    pygame.display.update()

pygame.time.delay(5000)

pygame.quit()