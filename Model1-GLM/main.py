import pygame
import time
import random

pygame.init()

# Set up the display window
width = 600
height = 400
gameDisplay = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake Game')

# Set up colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

clock = pygame.time.Clock()
game_over = False
game_close = False

snake_block = 10
snake_list = []
snake_length = 1

# Set up the initial position of the snake
x1 = width / 2
y1 = height / 2

x1_change = 0
y1_change = 0

# Set up the food
foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0

# Set up the game font
font_style = pygame.font.SysFont(None, 50)
score_font = pygame.font.SysFont(None, 35)

# Set up the score
score = 0

# Game loop
while not game_over:

    while game_close == True:
        gameDisplay.fill(blue)
        msg = font_style.render("You Lost! Press Q-Quit or C-Play Again", True, red)
        gameDisplay.blit(msg, [width / 2 - 150, height / 2 - 20])
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    game_over = True
                    game_close = False
                if event.key == pygame.K_c:
                    game_over = False
                    game_close = False
                    snake_list = []
                    snake_length = 1
                    x1 = width / 2
                    y1 = height / 2
                    x1_change = 0
                    y1_change = 0
                    foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
                    foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0
                    score = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x1_change = -snake_block
                y1_change = 0
            elif event.key == pygame.K_RIGHT:
                x1_change = snake_block
                y1_change = 0
            elif event.key == pygame.K_UP:
                y1_change = -snake_block
                x1_change = 0
            elif event.key == pygame.K_DOWN:
                y1_change = snake_block
                x1_change = 0

    # Check if the snake has hit the window border
    if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:
        game_close = True
    x1 += x1_change
    y1 += y1_change
    gameDisplay.fill(black)
    gameDisplay.blit(font_style.render('Score: ' + str(score), True, white), [0, 0])

    # Check if the snake has hit the food
    if x1 == foodx and y1 == foody:
        score += 1
        snake_length += 1
        foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
        foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0

    for x in snake_list[:-1]:
        if x[0] == x1 and x[1] == y1:
            game_close = True

    # Add the new block to the snake
    snake_head = []
    snake_head.append(x1)
    snake_head.append(y1)
    snake_list.append(snake_head)
    if len(snake_list) > snake_length:
        del snake_list[0]

    # Draw the snake
    for x in snake_list:
        pygame.draw.rect(gameDisplay, green, [x[0], x[1], snake_block, snake_block])

    # Draw the food
    pygame.draw.rect(gameDisplay, red, [foodx, foody, snake_block, snake_block])

    pygame.display.update()

    clock.tick(15)

pygame.quit()
quit()
