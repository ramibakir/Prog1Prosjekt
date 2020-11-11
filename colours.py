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


def get_colour(colour_name):
    for colour, value in colours.items():
        if colour_name == colour:
            return value
