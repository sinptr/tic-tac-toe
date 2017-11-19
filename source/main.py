import pygame
import sys
from source.constants import *
import collections

def load_picture(filepath):
    """
    :param      filepath: path to file

    :return:    picture: picture with size TILESIZE
    """
    picture = pygame.image.load(filepath)
    picture = pygame.transform.scale(picture, (TILESIZE, TILESIZE))
    return picture


def draw_grid(display_surf, width=1):
    """

    :param      display_surf: display surface
    :param      width: width of grid lines

    :return:
    drawing grid on game map
    """
    for y in range(MAPHEIGHT):
        for x in range(MAPWIDTH):
            rect = pygame.Rect(x * TILESIZE, y * TILESIZE, TILESIZE, TILESIZE)
            pygame.draw.rect(display_surf, (0, 0, 0), rect, width)


def exit_game():
    """

    :return:
    exit the game
    """
    pygame.display.quit()
    sys.exit()


def is_win(tilemap, active_cell):
    #TODO захерачить проверку на выигрыш, можно прыгать от последнего хода для оптисизации
    return  #winner


def element_count(el_list, element=EMPTY):
    try:
        count = collections.Counter(el_list)[element]
    except:
        count = 0
    finally:
        return count


def next_turn(tilemap, active_cell=0):
    #TODO захерачить определение следующего хода, возвращать tuple клетки в которую ходить
    return  #(x, y)


def get_active_cell(display_surf, mouse_pos):
    for row in range(MAPWIDTH):
        for column in range(MAPHEIGHT):
            if (column * TILESIZE) <= mouse_pos[0] <= (column * TILESIZE) + TILESIZE:
                if (row * TILESIZE) <= mouse_pos[1] <= (row * TILESIZE) + TILESIZE:
                    cell = (row, column)
                    return cell


def draw_msg(display_surf, text, pos, fontsize=13, color=(0, 0, 0)):
    myfont = pygame.font.SysFont("monospace", fontsize)
    label = myfont.render(text, 1, color)
    display_surf.blit(label, pos)
