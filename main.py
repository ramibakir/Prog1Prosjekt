import pygame
from pygame import mixer
import sys
import colours
import random


def set_ball_animation():
    # TODO: create ball class to remove variables from global namespace
    # variables is declared in local scope, now available in global namespace
    global ball_speed_x, ball_speed_y, player_score, opponent_score, score_time, opponent_length
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Reverse speed for y axis
    if ball.top <= 0 or ball.bottom >= screenH:
        ball_speed_y *= -1

    # Reverse speed for x axis
    if ball.left <= 0:
        player_score += 1
        score_time = pygame.time.get_ticks()
    elif ball.right >= screenW:
        opponent_score += 1
        score_time = pygame.time.get_ticks()

    # Set ball to collide with player or opponent rect
    if ball.colliderect(player) or ball.colliderect(opponent):
        ball_speed_x *= -1


def set_player_animation():
    # 22 minutes video
    player.y += player_speed

    # Prevent player from moving off screen
    if player.top <= 0:
        player.top = 0
    if player.bottom >= screenH:
        player.bottom = screenH


def set_opponent_animation():
    # Set logic for opponent to move
    if opponent.top < ball.y:
        opponent.top += opponent_speed
    if opponent.bottom > ball.y:
        opponent.bottom -= opponent_speed

    # Prevent opponent from moving off screen
    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= screenH:
        opponent.bottom = screenH


def ball_restart():
    global ball_speed_x, ball_speed_y, score_time, go

    # Set
    current_time = pygame.time.get_ticks()
    # Center the ball after it hits right or left wall
    ball.center = (int(screenW / 2), int(screenH / 2))

    # Count down for player to be ready
    if current_time - score_time < 700:
        tomato = pygame.image.load('images/tomato.png')
        game_screen.blit(tomato, (screenW / 2 - 10, screenH / 2 + 20))
    if 700 < current_time - score_time < 1400:
        lemon = pygame.image.load('images/lemon.png')
        game_screen.blit(lemon, (screenW / 2 - 10, screenH / 2 + 20))
    if 1400 < current_time - score_time < 2000:
        apple = pygame.image.load('images/apple.png')
        game_screen.blit(apple, (screenW / 2 - 10, screenH / 2 + 20))
    if 2000 < current_time - score_time < 3000:
        start = pygame.image.load('images/start.png')
        game_screen.blit(start, (screenW / 2 - 10, screenH / 2 + 20))
        mixer.music.play()

    # If result is less than 3 secs, set ball to not move
    if current_time - score_time < 3000:
        ball_speed_x, ball_speed_y = 0, 0
    else:
        # If result is greater than 3 secs, set ball to move randomly
        # Set ball to go in a random direction after reset
        ball_speed_y = 7 * random.choice((1, -1))
        ball_speed_x = 7 * random.choice((1, -1))
        score_time = None


# TODO: Add comment to describe what this is
pygame.mixer.pre_init(44100, -16, 1, 1024)
pygame.init()
clock = pygame.time.Clock()

go = mixer.music.load('sounds/go.wav')

screenW = 800
screenH = 600
game_screen = pygame.display.set_mode((screenW, screenH))
pygame.display.set_caption("Ping Pong")

game_end = False

# Save the length in variables to give powerups later
player_length = 140
opponent_length = 140

# Must be wrapped in an int to remove deprecation warning
ball = pygame.Rect(int(screenW / 2 - 15), int(screenH / 2 - 15), 30, 30)
player = pygame.Rect(int(screenW - 20), int(screenH / 2 - 70), 10, player_length)
opponent = pygame.Rect(10, int(screenH / 2 - 70), 10, opponent_length)

background_color = colours.get_colour("black")

ball_speed_x = 7 * random.choice((1, -1))
ball_speed_y = 7 * random.choice((1, -1))
player_speed = 0
opponent_speed = 7

player_score = 0
opponent_score = 0
top_score = 0
high_score = f"HIGH SCORE: {top_score}"

# Use SysFont() to use fonts without specifying path
game_font = pygame.font.SysFont("ARLRDBD.TTF", 32)
high_score_font = pygame.font.SysFont("ARLRDBD.TTF", 50)

# Score timer
# Will start timer first time game starts
score_time = True

# Game loop start
while not game_end:
    # Event loop start
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_end = False
            pygame.quit()
            # Has to be included, else pygame.error: display Surface quit will appear
            sys.exit()

        # Controls
        # Checks if ANY key is pressed
        if event.type == pygame.KEYDOWN:
            # Checks if the pressed key is arrow down
            if event.key == pygame.K_DOWN:
                player_speed += 7
            # Checks if the pressed key is arrow up
            if event.key == pygame.K_UP:
                player_speed -= 7

        # Checks if ANY key is released
        if event.type == pygame.KEYUP:
            # Checks if the released key is arrow down
            if event.key == pygame.K_DOWN:
                player_speed -= 7
            # Checks if the released key is arrow up
            if event.key == pygame.K_UP:
                player_speed += 7
    # Event loop end

    # Game logic
    # DO NOT DRAW INSIDE EVENT LOOP, WILL CAUSE MAJOR LAG
    set_ball_animation()
    set_player_animation()
    set_opponent_animation()

    # Set background color
    game_screen.fill(background_color)

    # Draw the shapes needed for the game
    pygame.draw.rect(game_screen, colours.get_colour("blue"), player)
    pygame.draw.rect(game_screen, colours.get_colour("green"), opponent)
    pygame.draw.ellipse(game_screen, colours.get_colour("gold"), ball)

    # Draw line to separate player and opponent
    pygame.draw.aaline(game_screen, colours.get_colour("grey"), (screenW / 2, 0), (screenW / 2, screenH))

    if score_time:
        ball_restart()

    # Create surface for text to be displayed, has to be below game_screen.fill
    player_text = game_font.render(f"{player_score}", False, colours.get_colour("white"))
    game_screen.blit(player_text, (440, 150))
    opponent_text = game_font.render(f"{opponent_score}", False, colours.get_colour("white"))
    game_screen.blit(opponent_text, (340, 150))
    high_score_text = game_font.render(f"{high_score}", False, colours.get_colour("white"))
    game_screen.blit(high_score_text, (343, 50))

    pygame.display.flip()
    clock.tick(60)
# Game loop end
