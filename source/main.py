import pygame
import sys
from source.constants import *
import collections
import numpy as np


def get_key(d, value):
    """
    :param      d: source dictionary

    :param      value: value in d

    :return:    k: key accordingly to value v
    """
    for k, v in d.items():
        if v == value:
            return k
    return 0


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
    pygame.display.quit()
    sys.exit()


def is_win(tilemap, coordinate_of_last_move):
    """
    :param      tilemap:    Game field

    :param      coordinate_of_last_move:    previous move

    :return:    CROSS if CROSS should be putted
                CIRCLE if CIRCLE should be putted
                False if can't determine next step
    """
    cc = element_count(tilemap[coordinate_of_last_move[0]])
    if cc.get(CROSS) == MAPWIDTH:
        return CROSS
    elif cc.get(CIRCLE) == MAPWIDTH:
        return CIRCLE
    trans = np.transpose(tilemap)
    cc = element_count(trans[coordinate_of_last_move[0]])
    if cc.get(CROSS) == MAPWIDTH:
        return CROSS
    elif cc.get(CIRCLE) == MAPWIDTH:
        return CIRCLE
    if coordinate_of_last_move[0] == coordinate_of_last_move[1]:
        pd = np.diag(tilemap)
        cc = element_count(pd)
        if cc.get(CROSS) == MAPWIDTH:
            return CROSS
        elif cc.get(CIRCLE) == MAPWIDTH:
            return CIRCLE
    if coordinate_of_last_move[0] == len(tilemap) - coordinate_of_last_move[1] - 1:
        spisok = [tilemap[i][len(tilemap) - 1 - i] for i in range(len(tilemap))]
        cc = element_count(spisok)
        if cc.get(CROSS) == MAPWIDTH:
            return CROSS
        elif cc.get(CIRCLE) == MAPWIDTH:
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


def get_row_same_state(arr):
    """
    :param      arr:    string list
                        strings from game field:
                            - rows,
                            - columns,
                            - diagonals

    :return:    (i, column): coordinates of next step
    """
    i = 0
    for row in arr:
        p = element_count(row)
        if get_key(p, MAPWIDTH - 1):
            break
        i += 1
    column = 0
    if i != len(arr):
        print(i)
        for j in arr[i]:
            if j == EMPTY:
                return i, column
            column += 1
    return 0


def two_dicks_in_one_chick(tilemap):
    """
    :param      tilemap:    Game field

    :return:    coord:      coordanates of next step

    For first situation in situation list: alchogorithm tic-tac-toe
    """
    # Rows
    coord = get_row_same_state(tilemap)
    if coord:
        return coord

    # Columns
    coord = get_row_same_state(list(np.transpose(tilemap)))
    if coord:
        return coord[1], coord[0]

    # Diagonals
    diags = list()
    diags.append(list(np.diag(tilemap)))
    diags.append([tilemap[i][len(tilemap) - 1 - i] for i in range(len(tilemap))])
    coord = get_row_same_state(diags)
    if coord:
        if coord[0] == 0:
            return coord[1], coord[1]
        else:
            return coord[1], MAPHEIGHT - 1 - coord[1]

    # Either
    return 0


def two_guys_one_cup(tilemap, last_move):
    if last_move in ((0, 0), (0, MAPWIDTH - 1), (MAPHEIGHT - 1, 0), (MAPHEIGHT - 1, MAPWIDTH - 1)):
        if last_move[0] == last_move[1]:
            if last_move[0] != MAPHEIGHT - 1:
                oposite_cell = MAPHEIGHT - 1, MAPWIDTH - 1
            else:
                oposite_cell = 0, 0
        else:
            if last_move[0] != MAPHEIGHT - 1:
                oposite_cell = MAPHEIGHT - 1, 0
            else:
                oposite_cell = 0, MAPWIDTH - 1
        if tilemap[oposite_cell[0]][oposite_cell[1]] == EMPTY:
            return oposite_cell
    return 0


def mfm(tilemap):
    if MAPWIDTH % 2 == MAPHEIGHT % 2 == 1:
        cell = MAPHEIGHT // 2, MAPWIDTH // 2
        if tilemap[cell[0]][cell[1]] == EMPTY:
            return cell
    return 0


def gangbang(tilemap):
    pussy = 0
    ass = 1
    chicks = ((0, 0), (0, MAPWIDTH - 1), (MAPHEIGHT - 1, 0), (MAPHEIGHT - 1, MAPWIDTH - 1))
    for bitch in chicks:
        if tilemap[bitch[pussy]][bitch[ass]] == EMPTY:
            return bitch
    return 0


def jerk_off(collection):
    for genre in range(MAPHEIGHT):
        for fetish in range(MAPWIDTH):
            if collection[genre][fetish] == EMPTY:
                return genre, fetish
    return 0


def next_turn(tilemap, last_move):
    """
    :param tilemap:
    :param active_cell:
    :return:
    """
    cell = two_dicks_in_one_chick(tilemap)
    if cell:
        return cell
    cell = mfm(tilemap)
    if cell:
        return cell
    cell = two_guys_one_cup(tilemap, last_move)
    if cell:
        return cell
    cell = gangbang(tilemap)
    if cell:
        return cell
    return jerk_off(tilemap)


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
