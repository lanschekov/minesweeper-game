from random import randint

import pygame
from pygame import Surface, SurfaceType

from BlackWhiteBoard import Board, BLACK_COLOR, WHITE_COLOR

MINED_CELL = 10
CLOSED_CELL = -1
MINED_COLOR = (255, 0, 0)
CLOSED_COLOR = BLACK_COLOR


class Minesweeper(Board):
    def __init__(self, width: int, height: int, mines_amount: int):
        super(Minesweeper, self).__init__(width, height)
        self.board = [[CLOSED_CELL] * width for _ in range(height)]
        self.mines_amount = mines_amount
        for _ in range(self.mines_amount):
            self.board[randint(0, self.height - 1)][randint(0, self.width - 1)] = MINED_CELL

    def render(self, screen: Surface | SurfaceType) -> None:
        screen.fill((0, 0, 0))
        cur_x, cur_y = self.x, self.y
        for row in self.board:
            for cell in row:
                # Cell borders
                pygame.draw.rect(screen, WHITE_COLOR,
                                 (cur_x, cur_y, self.cell_size, self.cell_size), width=1)
                # Cell pouring
                pygame.draw.rect(screen, MINED_COLOR if cell is MINED_CELL else CLOSED_COLOR,
                                 (cur_x + 1, cur_y + 1, self.cell_size - 2, self.cell_size - 2), width=0)

                if cell not in (MINED_CELL, CLOSED_CELL):
                    self.show_text(cell, cur_x, cur_y)
                cur_x += self.cell_size
            cur_x = self.x
            cur_y += self.cell_size

    def show_text(self, cell: int, cur_x: int, cur_y: int) -> None:
        font = pygame.font.Font(None, self.cell_size)
        text = font.render(str(cell), True, (0, 255, 0))
        screen.blit(text, (cur_x + 1, cur_y + 1))

    def on_click(self, cell_row: int, cell_col: int) -> None:
        self.open_cell(cell_row, cell_col)

    def open_cell(self, cell_row: int, cell_col: int) -> None:
        neighbors = self.get_neighbors(cell_row, cell_col)
        mined_amount = len([cell for cell in neighbors if cell is MINED_CELL])
        self.board[cell_row][cell_col] = mined_amount

    def get_neighbors(self, cell_row: int, cell_coll: int) -> tuple:
        res = []
        neighbors_ind = ((cell_row - 1, cell_coll - 1), (cell_row - 1, cell_coll),
                         (cell_row - 1, cell_coll + 1), (cell_row, cell_coll - 1),
                         (cell_row, cell_coll + 1), (cell_row + 1, cell_coll - 1),
                         (cell_row + 1, cell_coll), (cell_row + 1, cell_coll + 1))
        for row, col in neighbors_ind:
            if 0 <= row <= self.height - 1 and 0 <= col <= self.width - 1:
                res.append(self.board[row][col])
        return tuple(res)


if __name__ == '__main__':
    pygame.init()
    size = width, height = 800, 600
    screen = pygame.display.set_mode(size)

    board = Minesweeper(20, 20, 20)
    board.set_view(0, 0, 30)
    board.render(screen)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.get_click(*event.pos)

        board.render(screen)
        pygame.display.flip()

    pygame.quit()
