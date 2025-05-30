from color_code import *

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
TITLE = "Analog Clock"

BACKGROUND = 0,0,255
LINE = 255,255,255

H_WIDTH, H_HEIGHT = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
RADIUS = H_HEIGHT - 50
RADIUS_LIST = {'sec': RADIUS - 10, 'min': RADIUS - 55, 'hour': RADIUS - 100, 'digit': RADIUS - 30}
RADIUS_ARK = RADIUS + 8

GRAY_RING = GRAY

COLOR_RING_SECONDS = LIGHT_BLUE
COLOR_RING_MINUTES = TURQUOISE
COLOR_RING_HOURS = ORANGE
