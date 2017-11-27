from source.constants import *
from copy import deepcopy
import collections
import numpy as np
import pygame
import sys


def get_markup_matrix(coord_param, matrix_param):
    """
    :param      coord_param:    tuple (x, y)

    :param      matrix_param:   matrix to markup

    :return:    tmp_matrix:     markuped matrix

    Marks the x-th row and y-th column of tmp_matrix with *
    """
    tmp_matrix = matrix_param
    for i in range(len(tmp_matrix)):
        tmp_matrix[coord_param[0]][i] = '*'
    for j in range(len(tmp_matrix)):
        tmp_matrix[j][coord_param[1]] = '*'
    return tmp_matrix


def get_safe_copy(matrix_param):
    """
    :param      matrix_param:   some matrix

    :return:    Safe copy of matrix_param using copy.deepcopy() from copy module
    """
    return deepcopy(matrix_param)


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
        lst = [tilemap[i][len(tilemap) - 1 - i] for i in range(len(tilemap))]
        cc = element_count(lst)
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


def get_opposite_figure(figure_param):
    """
    :param      figure_param:   CROSS or CIRCLE

    :return:    Opposite figure for figure_param
    """
    return CROSS if figure_param == CIRCLE else CIRCLE


def second_rule(matrix_param, prev_step):
    """
    :param      matrix_param:   game field

    :param      prev_step:      coordinates of previous step

    :return:    coordinates of next step

    Title 2 from algo.doc.
    Creates two lines with two markups
    """
    if matrix_param[prev_step[0]][prev_step[1]] == CROSS:
        current_figure = CIRCLE
    else:
        current_figure = CROSS
    for i in range(len(matrix_param)):
        for j in range(len(matrix_param)):
            if matrix_param[i][j] == current_figure:
                less_matrix = get_markup_matrix((i, j), get_safe_copy(matrix_param))
                for p in range(len(less_matrix)):
                    for q in range(len(less_matrix)):
                        if less_matrix[p][q] == current_figure:
                            if matrix_param[i][q] != CIRCLE and matrix_param[i][q] != CROSS:
                                if not (element_count(matrix_param[p], get_opposite_figure(current_figure))):
                                    return i, q
                            if matrix_param[p][j] != CIRCLE and matrix_param[p][j] != CROSS:
                                if not (element_count(np.transpose(matrix_param)[q],
                                                      get_opposite_figure(current_figure))):
                                    return p, j
    return 0


def track_duplicates(matrix_param):
    """
    :param      matrix_param: some matrix

    :return:    (i, column) or 0

    Finds the duplicates elements if matrix_param, and returns coordinate's tuple (i, column)
    which is placed in lane with duplicates with empty slot in (i, column) - coordinates.

    If there's no line with such properties returns 0
    """
    i = 0
    for row in matrix_param:
        p = element_count(row)
        if get_key(p, 2) and get_key(p, 1) == EMPTY:
            break
        i += 1
    column = 0
    if i != len(matrix_param):
        for j in matrix_param[i]:
            if j == 0:
                return i, column
            column += 1
    return 0


def first_rule(tilemap):
    """
    :param      tilemap:    Game field

    :return:    coord:      coordinates of next step

    Title 1 from algo.doc.
    Creates one fully filled line.
    """
    coord = track_duplicates(tilemap)
    if coord:
        return coord
    coord = track_duplicates(list(np.transpose(tilemap)))
    if coord:
        return coord[1], coord[0]
    diags = list()
    diags.append(list(np.diag(tilemap)))
    diags.append([tilemap[i][len(tilemap) - 1 - i] for i in range(len(tilemap))])
    coord = track_duplicates(diags)
    if coord:
        if coord[0] == 0:
            return coord[1], coord[1]
        else:
            return coord[1], MAPHEIGHT - 1 - coord[1]
    return 0


def fourth_rule(tilemap, last_move):
    """
    :param      tilemap: game field

    :param      last_move: previous step

    :return:    coordinates of the next step

    Title 4 from algo.doc.
    Places the mark in opposite angle to enemy's angle
    """
    if last_move in ((0, 0), (0, MAPWIDTH - 1), (MAPHEIGHT - 1, 0), (MAPHEIGHT - 1, MAPWIDTH - 1)):
        if last_move[0] == last_move[1]:
            if last_move[0] != MAPHEIGHT - 1:
                opposite_cell = MAPHEIGHT - 1, MAPWIDTH - 1
            else:
                opposite_cell = 0, 0
        else:
            if last_move[0] != MAPHEIGHT - 1:
                opposite_cell = MAPHEIGHT - 1, 0
            else:
                opposite_cell = 0, MAPWIDTH - 1
        if tilemap[opposite_cell[0]][opposite_cell[1]] == EMPTY:
            return opposite_cell
    return 0


def third_rule(tilemap):
    """
    :param      tilemap:    game field

    :return:    cell:       (x, y)

    Title 3 from algo.doc.
    Places figure in central cell.
    """
    if MAPWIDTH % 2 == MAPHEIGHT % 2 == 1:
        cell = MAPHEIGHT // 2, MAPWIDTH // 2
        if tilemap[cell[0]][cell[1]] == EMPTY:
            return cell
    return 0


def fifth_rule(tilemap):
    """
    :param      tilemap: Game field

    :return:    option: coordinates of next step

    Title 5 from algo.doc.
    Places mark in free angle cell.
    """
    options = ((0, 0), (0, MAPWIDTH - 1), (MAPHEIGHT - 1, 0), (MAPHEIGHT - 1, MAPWIDTH - 1))
    for option in options:
        if tilemap[option[0]][option[1]] == EMPTY:
            return option
    return 0


def sixth_rule(tilemap):
    """
    :param      tilemap:    game field

    :return:    (i, j):     next empty cell coordinates

    Title 6 from algo.doc.
    Places the mark in first empty found cell
    """
    for i in range(MAPHEIGHT):
        for j in range(MAPWIDTH):
            if tilemap[i][j] == EMPTY:
                return i, j
    return 0


def next_turn(tilemap, last_move):
    """
    :param      tilemap: Game field

    :param      last_move: previous move

    :return:    cell: (x, y)
    """
    cell = first_rule(tilemap)
    if cell:
        print('first_rule')
        return cell
    cell = second_rule(tilemap, last_move)
    if cell:
        print('second_rule')
        return cell
    cell = third_rule(tilemap)
    if cell:
        print('third_rule')
        return cell
    cell = fourth_rule(tilemap, last_move)
    if cell:
        print('fourth')
        return cell
    cell = fifth_rule(tilemap)
    if cell:
        print('fifth_rule')
        return cell
    print('sixth_rule')
    return sixth_rule(tilemap)


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
