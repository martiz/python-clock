import pygame
from datetime import datetime
import math
import sys
from constants import *

def main():

    # Initialize Pygame
    pygame.init()
    # Screen dimensions / info
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()

    clock60 = dict(zip(range(60), range(0, 360, 6)))  # for hours, minutes and seconds

    def get_clock_pos(clock_dict, clock_hand, key):
        x = H_WIDTH + RADIUS_LIST[key] * math.cos(math.radians(clock_dict[clock_hand]) - math.pi / 2)
        y = H_HEIGHT + RADIUS_LIST[key] * math.sin(math.radians(clock_dict[clock_hand]) - math.pi / 2)
        return x, y

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

        screen.fill((BACKGROUND))

        # get time now
        t = datetime.now()
        hour, minute, second = ((t.hour % 12) * 5 + t.minute // 12) % 60, t.minute, t.second
        # draw face
        for digit, pos in clock60.items():
            radius = 20 if not digit % 3 and not digit % 5 else 8 if not digit % 5 else 2
            pygame.draw.circle(screen, pygame.Color('gainsboro'), get_clock_pos(clock60, digit, 'digit'), radius, 7)
        # draw clock
        pygame.draw.line(screen, pygame.Color('orange'), (H_WIDTH, H_HEIGHT), get_clock_pos(clock60, hour, 'hour'), 15)
        pygame.draw.line(screen, pygame.Color('green'), (H_WIDTH, H_HEIGHT), get_clock_pos(clock60, minute, 'min'), 7)
        pygame.draw.line(screen, pygame.Color('magenta'), (H_WIDTH, H_HEIGHT), get_clock_pos(clock60, second, 'sec'), 4)
        pygame.draw.circle(screen, pygame.Color('white'), (H_WIDTH, H_HEIGHT), 8)
        # draw arc
        sec_angle = -math.radians(clock60[t.second]) + math.pi / 2
        pygame.draw.arc(screen, pygame.Color('yellow'),
            (H_WIDTH - RADIUS_ARK, H_HEIGHT - RADIUS_ARK, 2 * RADIUS_ARK, 2 * RADIUS_ARK), math.pi / 2, sec_angle, 8)

        pygame.display.flip()
        clock.tick(20)

if __name__ == "__main__":
    main()
