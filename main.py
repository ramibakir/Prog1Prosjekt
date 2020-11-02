import pygame
import sys
import colours
import random


def set_ball_animation():
    # ball_speed is declared in local scope, now available in global namespace
    global ball_speed_x, ball_speed_y
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Reverse speed for y axis
    if ball.top <= 0 or ball.bottom >= screenH:
        ball_speed_y *= -1

    # Reverse speed for x axis
    if ball.left <= 0 or ball.right >= screenW:
        ball_restart()

    # Set ball to collide with player or opponent rects
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
    global ball_speed_x, ball_speed_y
    # Center the ball after it hits right or left wall
    ball.center = (int(screenW / 2), int(screenH / 2))
    # Set ball to go in a random direction after reset
    ball_speed_y *= random.choice((1, -1))
    ball_speed_x *= random.choice((1, -1))


pygame.init()
clock = pygame.time.Clock()

screenW = 800
screenH = 600
game_screen = pygame.display.set_mode((screenW, screenH))
pygame.display.set_caption("Ping Pong")

game_end = False

# Must be wrapped in an int to remove deprecation warning
ball = pygame.Rect(int(screenW / 2 - 15), int(screenH / 2 - 15), 30, 30)
player = pygame.Rect(int(screenW - 20), int(screenH / 2 - 70), 10, 140)
opponent = pygame.Rect(10, int(screenH / 2 - 70), 10, 140)

background_color = colours.get_colour("black")

ball_speed_x = 7 * random.choice((1, -1))
ball_speed_y = 7 * random.choice((1, -1))
player_speed = 0
opponent_speed = 7

while not game_end:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_end = False
            pygame.quit()
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
        if event.type == pygame.KEYDOWN:
            # Checks if the released key is arrow down
            if event.key == pygame.K_DOWN:
                player_speed -= 7
            # Checks if the released key is arrow up
            if event.key == pygame.K_UP:
                player_speed += 7

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

    pygame.display.flip()
    clock.tick(60)
