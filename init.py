from source.main import *
from pygame.locals import *

tilemap = [[EMPTY for _ in range(MAPWIDTH)] for __ in range(MAPHEIGHT)]
pygame.init()
surf = pygame.display.set_mode((MAPWIDTH*TILESIZE, MAPHEIGHT*TILESIZE))
surf.fill((255, 255, 255))
cross = load_picture('images/cross.bmp')
circle = load_picture('images/circle.bmp')
flag = 0
draw_grid(surf)
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit_game()
        elif event.type == MOUSEBUTTONDOWN:

            mouse_pos = pygame.mouse.get_pos()
            act_cell = get_active_cell(mouse_pos)
            if tilemap[act_cell[0]][act_cell[1]] == EMPTY:
                flag = not flag
                picture = cross if flag else circle
                tilemap[act_cell[0]][act_cell[1]] = CROSS if flag else CIRCLE
                surf.blit(picture, (act_cell[1] * TILESIZE, act_cell[0] * TILESIZE, TILESIZE, TILESIZE))
                next_turn(tilemap, act_cell)
            print(tilemap)
    pygame.display.update()

