from datetime import datetime
import pygame
import sys
import colours
import random
import json

# Initialize pygame
pygame.init()
# Set screen size and specify pygame display to be this size
# also set background colour of screen to be black
screenW, screenH = 800, 600
menu_screen = pygame.display.set_mode((screenW, screenH))
menu_screen.fill(colours.get_colour('faded-black'))


# Create a dict where key is players to store
# name, points and date of win in array


def render_text(text, size, colour):
    """Render text on surface

    :text: String to render
    :size: Font-size to render text in
    :colour: Colour of text
    :return: Surface which text is printed on
    """
    font = pygame.font.Font('PressStart2P-Regular.ttf', size)
    text_surface = font.render(text, False, colours.get_colour(colour))

    return text_surface


def exit_game():
    pygame.quit()
    # Has to be included, else pygame.error: display Surface quit will appear
    sys.exit()


def blit_text(text, font_colour, font_size, x_pos, y_pos):
    menu_screen.blit(render_text(text, font_size, font_colour), (x_pos, y_pos))


# Define buttons and draw to screen
button_start = pygame.Rect(300, 420, 200, 30)
button_score = pygame.Rect(300, 480, 200, 30)
pygame.draw.rect(menu_screen, colours.get_colour('red'), button_start)
pygame.draw.rect(menu_screen, colours.get_colour('blue'), button_score)

# Add text to screen
menu_screen.blit(render_text('MAIN MENU', 30, 'white'), (270, 150))

# Add text to button_start
start_text = render_text('START', 18, 'black')
button_start_text = start_text.get_rect()
button_start_text.center = button_start.center
menu_screen.blit(start_text, button_start_text)

# Add text to button_score
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
                menu_screen.fill(colours.get_colour('black'))
                # Opens file in read mode and iterates through file
                # and gives variables data based on key specified
                scores_file = open('high-score1.json', 'r')
                score_data = json.loads(scores_file.read())
                for data in score_data['players']:
                    name_of_player = data['name']
                    points = data['wins']
                    date_of_win = data['date']
                    print(f'{name_of_player}: {points} on {date_of_win}')
                    # Add scores from file to screen, should print each score underneath the previous one.
                    # Right now, it prints both lines from file on top of each other.
                    blit_text(f'{name_of_player}: {points} on {date_of_win}', 'white', 15, 50, 50 + 20)

        elif event.type == pygame.KEYDOWN:
            # If ESC key is pressed while on high score screen
            # will exit menu loop and start game
            if event.key == pygame.K_ESCAPE:
                menu_active = False

# Set a new screen to be used for the rest of the game
game_screen = pygame.display.set_mode((screenW, screenH))


def game_over():
    """Exits game when one player reaches 5 points
    If player reaches 5 first, the player has to
    input their name in the terminal for the score
    to be saved with their name in file.

    Screen should display game over text with player name
    or Computer with the score
    """
    global game_end

    now = datetime.utcnow()
    win_time = now.strftime("%d/%m/%Y")

    # Opens file in append mode if it exists, if not the file will be created
    if player_score == 5:
        # At game end, player will be asked to type their name in the terminal
        player_name = input("Enter your name in the terminal below: ")

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
    """Animating the ball and setting collisions.
    Makes use of variables declared in global scope.

    Sets x and y pos of ball to be equal to a speed of 7,

    If ball hits left or right wall points will be given
    to the scorer
    """
    # variables is declared in local scope, now available in global namespace
    global ball_speed_x, ball_speed_y, player_score, opponent_score, score_time

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
    global ball_speed_x, ball_speed_y, score_time

    # Set
    current_time = pygame.time.get_ticks()
    # Center the ball after it hits right or left wall
    ball.center = (int(screenW / 2), int(screenH / 2))

    # Count down for player to be ready
    if current_time - score_time < 700:
        tomato = pygame.image.load('images/tomato.png')
        game_screen.blit(tomato, (350, 250))
    if 700 < current_time - score_time < 1400:
        lemon = pygame.image.load('images/lemon.png')
        game_screen.blit(lemon, (350, 250))
    if 1400 < current_time - score_time < 2000:
        apple = pygame.image.load('images/apple.png')
        game_screen.blit(apple, (350, 250))
    if 2000 < current_time - score_time < 3000:
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
        score_time = None


pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption("Ping Pong")

# Must be wrapped in an int to remove deprecation warning.
# Define objects the objects that are essential to the game
ball = pygame.Rect((int(screenW / 2 - 15), int(screenH / 2 - 15), 30, 30))
player = pygame.Rect(int(screenW - 20), int(screenH / 2 - 70), 10, 140)
opponent = pygame.Rect(10, int(screenH / 2 - 70), 10, 140)

ball_speed_x = 7 * random.choice((1, -1))
ball_speed_y = 7 * random.choice((1, -1))
player_speed = 0
opponent_speed = 7

player_score = 0
opponent_score = 0

# Score timer - will start the first time the game starts
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
    game_over()

    # Set background color
    game_screen.fill(colours.get_colour("faded-black"))

    # Draw the shapes needed for the game
    pygame.draw.rect(game_screen, colours.get_colour("blue"), player)
    pygame.draw.rect(game_screen, colours.get_colour("green"), opponent)
    pygame.draw.ellipse(game_screen, colours.get_colour("gold"), ball)

    # Draw line to separate player and opponent
    pygame.draw.aaline(game_screen, colours.get_colour("grey"), (screenW / 2, 0), (screenW / 2, screenH))

    #
    if score_time:
        ball_restart()

    # Create surface for text to be displayed, has to be below game_screen.fill
    game_screen.blit(render_text(f"{player_score}", 25, 'white'), (440, 200))
    game_screen.blit(render_text(f"{opponent_score}", 25, 'white'), (340, 200))

    # Opens file in reading mode and sets the first entry of file
    # at the top of the game screen during gameplay

    scores_file = open('high-score1.json', 'r')
    score_data = json.loads(scores_file.read())
    name_of_player = score_data['players'][0]['name']
    points = score_data['players'][0]['score']
    date_of_win = score_data['players'][0]['date']
    game_screen.blit(render_text(f'{name_of_player} won - {points} on {date_of_win}', 15, 'white'), (65, 50))

    pygame.display.flip()
    clock.tick(60)
# Game loop end
