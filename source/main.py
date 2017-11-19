import pygame
import sys
from source.constants import *
import collections
import numpy as np

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

    Drawing grid on game map
    """
    for y in range(MAPHEIGHT):
        for x in range(MAPWIDTH):
            rect = pygame.Rect(x * TILESIZE, y * TILESIZE, TILESIZE, TILESIZE)
            pygame.draw.rect(display_surf, (0, 0, 0), rect, width)


def exit_game():
    """

    :return:
    """
    pygame.display.quit()
    sys.exit()


def is_win(tilemap, coordinate_of_last_move):
    """
    BY PIOTR SLENKEN
    :param tilemap:
    :param coordinate_of_last_move:
    :return:
    """
    cc = element_count(tilemap[coordinate_of_last_move[0]])
    if cc.get(CROSS) == MAPWIDTH:
        return CROSS
    elif cc.get(CIRCLE) == MAPWIDTH:
        return CIRCLE
    print('column')

    trans = np.transpose(tilemap)
    cc = element_count(trans[coordinate_of_last_move[0]])
    if cc.get(CROSS) == MAPWIDTH:
        return CROSS
    elif cc.get(CIRCLE) == MAPWIDTH:
        return CIRCLE
    print('diag')

    markdown = 0
    if coordinate_of_last_move[0] == coordinate_of_last_move[1]:
        #TODO: Получить главную диагональ и считать количество элементов с помощью функции гет элеент каунт
        pd = np.trace(tilemap) / len(tilemap)
        print(pd)
        if pd == CROSS:
            return CROSS
        elif pd == CIRCLE:
            return CIRCLE
    print('subrow')
    if coordinate_of_last_move[0] == len(tilemap) + markdown - coordinate_of_last_move[1] - 1:
        spisok = [tilemap[i][len(tilemap) + markdown - 1 - i] for i in range(len(tilemap))]
        print('sosi')
        s = sum(spisok)
        pd = s / len(tilemap)
        if pd == CROSS:
            return CROSS
        elif pd == CIRCLE:
            return CIRCLE

    return False


def element_count(el_list, element=None):
    """
    :param      el_list:    list of elements

    :param      element:    element

    :return:    count: count of element in el_list
    """
    collection = collections.Counter(el_list)
    if element is None:
        return collection
    count = collection.get(element)
    if count is None:
        count = 0
    return count


def next_turn(tilemap, active_cell=0):
    """

    :param tilemap:
    :param active_cell:
    :return:
    """
    #TODO захерачить определение следующего хода, возвращать tuple клетки в которую ходить
    return  #(x, y)


def get_active_cell(mouse_pos):
    """
    :param      mouse_pos:  mouse position on widow screen

    :return:    cell:   cell... just cell
    """
    for row in range(MAPWIDTH):
        for column in range(MAPHEIGHT):
            if (column * TILESIZE) <= mouse_pos[0] <= (column * TILESIZE) + TILESIZE:
                if (row * TILESIZE) <= mouse_pos[1] <= (row * TILESIZE) + TILESIZE:
                    cell = (row, column)
                    return cell


def draw_msg(display_surf, text, pos, fontsize=13, color=(0, 0, 0)):
    """
    :param display_surf:   surface on which we display da message

    :param          text:           message text which we display message on surface on which we
                                display da message

    :param      pos:            position of the message text which we display message on surface on
                                which we
                                display da message

    :param      fontsize:       size of the font of position of the message text which we display message
                                on surface on which we display da message

    :param      color:

    :return:
    """
    myfont = pygame.font.SysFont("monospace", fontsize)
    label = myfont.render(text, 1, color)
    display_surf.blit(label, pos)
