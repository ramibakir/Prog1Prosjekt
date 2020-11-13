import json
import random
import sys
from datetime import datetime

import pygame


def get_colour(colour_name):
    """ Method which returns an RGB value
    of a colour from the list based on the name colour.

    Takes a string as parameter which is the colour name
    and returns the value if that colour is available in the list

    If colour is not available it will print that the specified colour
    is not in the list."""
    colours = {
        "white": (255, 255, 255),
        "black": (0, 0, 0),
        "red": (255, 0, 0),
        "gold": (239, 229, 51),
        "blue": (78, 162, 196),
        "grey": (170, 170, 170),
        "green": (77, 206, 145),
        'faded-black': (54, 54, 64)
    }

    for colour, value in colours.items():
        if colour_name == colour:
            return value
        elif colour_name not in colours:
            print(f'{colour_name} is not available in the list')


def render_text(text, size, colour):
    """Render text on surface

    :text: String to render
    :size: Font-size to render text in
    :colour: Colour of text
    :return: Surface which text is rendered on
    """
    font = pygame.font.Font('PressStart2P-Regular.ttf', size)
    text_surface = font.render(text, False, get_colour(colour))

    return text_surface


def exit_game():
    pygame.quit()
    # Has to be included, else pygame.error: display Surface quit will appear
    sys.exit()


def game_over():
    """Exits game when one player reaches 5 points
    If player reaches 5 first, the player has to
    input their name in the terminal for the score
    to be saved with their name in file. Name cannot be empty.

    Screen should display game over text with player name
    or Computer with the score -> is barley visible.

    When saving the file, a copy of the previous content will
    be made which the updated values will be appended to. The
    previous content will then be overwritten with the updates."""
    global game_end, win_time

    # Opens file in append mode if it exists, if not the file will be created
    if player_score == 5:
        # At game end, player will be asked to type their name in the terminal.
        # Players cannot leave name empty and have to type a name for the game to finish
        player_name = input("Enter your name in the terminal below: ")
        if player_name == "":
            print("Name can't be empty")
        else:
            # Add GAME OVER to screen, appears for one second (barely visible).
            game_screen.blit(render_text(f"GAME OVER - {player_name} won with {player_score} points", 15, 'white'),
                             (55, 50))

            with open('high-score1.json') as f_game_over:
                info = json.load(f_game_over)
            # Gets top level of json file
            json_top_level = info['players']

            # Sets new values inside dict to be appended
            # to json_top_level
            score_updates = {
                'name': player_name,
                'score': f'{player_score} points',
                'date': win_time
            }

            # Appends the value of player_name, player_score and win_time to file on the player key
            json_top_level.append(score_updates)

            # Writes the values to the file.
            # Will make a copy of content before overwriting
            # previous values so that the new values
            # will properly align inside player block
            with open('high-score1.json', 'w') as w_file:
                json.dump(info, w_file, ensure_ascii=False, indent=4)

            game_end = False
            exit_game()
    elif opponent_score == 5:
        # Add GAME OVER to screen, appears for one second (barely visible).
        game_screen.blit(render_text(f"GAME OVER - Computer won with {opponent_score} points", 15, 'white'),
                         (50, 50))
        game_end = False
        exit_game()


def set_ball_animation():
    """Animates the ball and sets collisions.
    Makes use of variables declared in global scope.

    Sets x and y pos of ball to be equal to a speed of 7.
    The ball will then move with a speed of 7 at 60fps,
    making it a moving ball.

    If ball hits left or right wall points will be given
    to the scorer

    If the ball hits bottom or top edge the vertical speed
    will be set as negative so that the ball does not disappear
    outside of the screen.
    """
    # variables is declared in local scope, now available in global namespace
    # Has to be the top level of the function
    global ball_speed_x, ball_speed_y, player_score, opponent_score, score_time

    # Set the x and y coordinates of the ball
    # to equal value of ball_speed_x and ball_speed_y
    # so that the ball can start moving
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Reverses the vertical ball speed
    # so that the ball "bounces off" the edge
    if ball.top <= 0 or ball.bottom >= screenH:
        ball_speed_y *= -1
    # Gives either player or opponent if
    # ball hits one of the edges
    elif ball.left <= 0:
        player_score += 1
        score_time = pygame.time.get_ticks()
    elif ball.right >= screenW:
        opponent_score += 1
        score_time = pygame.time.get_ticks()

    # If ball collides with player or opponent, the vertical speed
    # will be set as negative so that the ball "bounces off"
    if ball.colliderect(player) or ball.colliderect(opponent):
        ball_speed_x *= -1


def set_player_animation():
    """ Method which controls how player_movement is handled.

    For player to be able to move up or down, the y position of
    the player rect is initially set to 0, but will change when
    the game registers click event on arrow keys which triggers
    the speed to change.

    Will prevent player from going off the screen by setting
    the top position of the player rect to be the top edge of the screen (0)
    or the bottom position of the player rect to be the equal to the screen height(600)."""

    player.y += player_speed

    # Prevent player from moving off screen
    if player.top <= 0:
        player.top = 0
    elif player.bottom >= screenH:
        player.bottom = screenH


def set_opponent_animation():
    """ Method for the opponent to move
    and prevents them from moving off screen.

    Opponent rect will move upwards if the top position
    is less than the y position of the ball. Downwards
    movement will be determined if the
    bottom position of the opponent rect is greater
    than the y position of the ball.

    Will prevent opponent from going off the screen by setting
    the top position of the opponent rect to be the top edge of the screen (0)
    or the bottom position of the opponent rect to be the equal to the screen height(600)."""

    # Set logic for opponent to move
    if opponent.top < ball.y:
        opponent.top += opponent_speed
    elif opponent.bottom > ball.y:
        opponent.bottom -= opponent_speed

    # Prevent opponent from moving off screen
    if opponent.top <= 0:
        opponent.top = 0
    elif opponent.bottom >= screenH:
        opponent.bottom = screenH


def ball_restart():
    """ Function to which sets the ball to the center of the screen
    if player or opponent scores a point.

    For the ball to change direction after being set to the center
    we multiply the vertical and horizontal speed with either
    1 or -1 so that the direction is the ball goes after reset is
    randomized.

    Includes a timer which blit(s) images to the screen which
    acts as a countdown for the player to be ready.

    If a point has been scored and the time between score_time
    and current_time is less than 3 seconds ball will not move.
    If it is more, ball will move in a random direction. """
    global ball_speed_x, ball_speed_y, score_time

    # Set the value to be the time since
    # pygame.init() was called, at that specific moment
    current_time = pygame.time.get_ticks()
    # Center the ball after it hits right or left wall
    ball.center = (int(screenW / 2), int(screenH / 2))

    # Count down for player to be ready. Displays
    # image if the result of current_time - score_time
    # is greater than the left value or less than the right value
    if current_time - score_time < 500:
        tomato = pygame.image.load('images/tomato.png')
        game_screen.blit(tomato, (350, 250))
    elif 500 < current_time - score_time < 1000:
        lemon = pygame.image.load('images/lemon.png')
        game_screen.blit(lemon, (350, 250))
    elif 1000 < current_time - score_time < 2000:
        apple = pygame.image.load('images/apple.png')
        game_screen.blit(apple, (350, 250))
    elif 2000 < current_time - score_time < 3000:
        start = pygame.image.load('images/start.png')
        game_screen.blit(start, (280, 250))

    # If result is less than 3 secs, set ball to not move
    if current_time - score_time < 3000:
        ball_speed_x, ball_speed_y = 0, 0
    else:
        # If result is greater than 3 secs, set ball to move randomly
        # Set ball to go in a random direction after reset
        ball_speed_y = 7 * random.choice((1, -1))
        ball_speed_x = 7 * random.choice((1, -1))
        # When set to None will prevent ball from
        # moving when the game starts the first time
        score_time = None


# Initialize pygame
pygame.init()
pygame.display.set_caption("Pong Menu")
# Set screen size and specify pygame display to be this size
# also set background colour of screen to be black
screenW, screenH = 800, 600
menu_screen = pygame.display.set_mode((screenW, screenH))
menu_screen.fill(get_colour('faded-black'))

# Get a date for saving the score
# and use it in d/m/y format
now = datetime.utcnow()
win_time = now.strftime("%d/%m/%Y")

# Define buttons and draw to screen
button_start = pygame.Rect(300, 420, 200, 30)
button_score = pygame.Rect(300, 480, 200, 30)
pygame.draw.rect(menu_screen, get_colour('red'), button_start)
pygame.draw.rect(menu_screen, get_colour('blue'), button_score)

# Add text to screen
menu_screen.blit(render_text('MAIN MENU', 30, 'white'), (270, 150))

# Add text to button_start by creating a surface
# for the text to be placed on top of
start_text = render_text('START', 18, 'black')
button_start_text = start_text.get_rect()
button_start_text.center = button_start.center
menu_screen.blit(start_text, button_start_text)

# Add text to button_score by creating a surface
# for the text to be placed on top of
score_text = render_text('HIGH SCORE', 18, 'black')
button_score_text = score_text.get_rect()
button_score_text.center = button_score.center
menu_screen.blit(score_text, button_score_text)

# Flag for menu loop
menu_active = True

# Separate loop for menu which includes buttons for starting game and viewing high score
# At click on START button, menu loop will end and closes this window. Opens up a new window
# where game loop will run
while menu_active:
    pygame.display.flip()
    # Get x,y position of mouse
    mx, my = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit_game()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Checks if position of mouse is between coordinates of button
            # and if it is clicked. On click will break menu loop and start game
            if 300 < mx <= 500 and 420 < my <= 450:
                menu_active = False
                pygame.quit()
                break
            elif 300 < mx <= 500 and 480 < my <= 510:
                # Checks if position of mouse is between coordinates of button
                # and if it is clicked. On click will break menu loop and show high score screen
                menu_screen.fill(get_colour('black'))
                # Opens file in read mode and iterates through file
                # and gives variables data based on key specified
                scores_file = open('high-score1.json', 'r')
                score_data = json.loads(scores_file.read())
                # Set y position of the text to be a constant
                y_pos = 50
                for data in score_data['players']:
                    name_of_player = data['name']
                    points = data['score']
                    date_of_win = data['date']
                    # Add scores from file to screen
                    menu_screen.blit(render_text(f'{name_of_player}: {points} on {date_of_win}', 20, 'white'),
                                     (50, y_pos))
                    # For every text that has been blit to screen y_pos will have an added 30 px so that
                    # the text moves down the previous value of y_pos + 30 (1: 50 + 30 = 80, 2: 80 + 30 = 110 ++)
                    y_pos += 30

        elif event.type == pygame.KEYDOWN:
            # If ESC key is pressed while on high score screen
            # will exit menu loop and start game
            if event.key == pygame.K_ESCAPE:
                menu_active = False

# Set a new screen to be used for the rest of the game
game_screen = pygame.display.set_mode((screenW, screenH))

pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption("Pong Game")

# Must be wrapped in an int to remove deprecation warning.
# Define objects the objects that are essential to the game
ball = pygame.Rect((int(screenW / 2 - 15), int(screenH / 2 - 15), 30, 30))
player = pygame.Rect(int(screenW - 20), int(screenH / 2 - 70), 10, 140)
opponent = pygame.Rect(10, int(screenH / 2 - 70), 10, 140)

# Variables for horizontal and vertical ball speed
# so that the ball moves in a random direction when
# the game starts
ball_speed_x = 7 * random.choice((1, -1))
ball_speed_y = 7 * random.choice((1, -1))

# Variables to set speed of player and opponent rect
# so that they can move. player_speed is 0 so that
# we can control movement with arrow keys.
player_speed = 0
opponent_speed = 5

# Variables to keep track of score so that we can end game
# at specific score
player_score = 0
opponent_score = 0

# If true, will start the timer found in ball_restart()
# method, when the game starts for the first time
score_time = True

# Flag for game loop
game_end = False

# Game loop start
while not game_end:
    # Event loop start
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_end = False
            exit_game()
        # Controls
        # Checks if ANY key is pressed down
        elif event.type == pygame.KEYDOWN:
            # Checks if the pressed key is arrow down
            if event.key == pygame.K_DOWN:
                player_speed += 7
            # Checks if the pressed key is arrow up
            elif event.key == pygame.K_UP:
                player_speed -= 7
        # Checks if ANY key is released
        elif event.type == pygame.KEYUP:
            # Checks if the released key is arrow down
            if event.key == pygame.K_DOWN:
                player_speed -= 7
            # Checks if the released key is arrow up
            elif event.key == pygame.K_UP:
                player_speed += 7
    # Event loop end

    # Game logic
    # DO NOT DRAW INSIDE EVENT LOOP, WILL CAUSE MAJOR LAG
    set_ball_animation()
    set_player_animation()
    set_opponent_animation()
    game_over()

    # Set background color
    game_screen.fill(get_colour("faded-black"))

    # Draw the shapes needed for the game
    pygame.draw.rect(game_screen, get_colour("blue"), player)
    pygame.draw.rect(game_screen, get_colour("green"), opponent)
    pygame.draw.ellipse(game_screen, get_colour("gold"), ball)

    # Draw line to separate player and opponent
    pygame.draw.aaline(game_screen, get_colour("grey"), (screenW / 2, 0), (screenW / 2, screenH))

    # If true, will keep
    # running method so that the
    # current_time variable can
    # keep track of the time since pygame.init()
    if score_time:
        ball_restart()

    # Create surface for text to be displayed, has to be below game_screen.fill
    game_screen.blit(render_text(f"{player_score}", 25, 'white'), (440, 200))
    game_screen.blit(render_text(f"{opponent_score}", 25, 'white'), (340, 200))

    # Opens file in reading mode and sets the first entry of file
    # at the top of the game screen during gameplay.
    scores_file = open('high-score1.json', 'r')
    score_data = json.loads(scores_file.read())
    name_of_player = score_data['players'][0]['name']
    points = score_data['players'][0]['score']
    date_of_win = score_data['players'][0]['date']
    game_screen.blit(render_text(f'{name_of_player} won - {points} on {date_of_win}', 15, 'white'), (135, 50))

    pygame.display.flip()
    clock.tick(60)
# Game loop end
