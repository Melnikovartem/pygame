import pygame
import random

# creating the data structure for pieces
# setting up global vars
# functions
# - create_grid
# - draw_grid
# - draw_window
# - rotating shape in main
# - setting up the main

"""
10 x 20 square grid
shapes: S, Z, I, O, J, L, T
represented in order by 0 - 6
"""

pygame.font.init()

# GLOBALS VARS
s_width = 800
s_height = 700
play_width = 300  # meaning 300 // 10 = 30 width per block
play_height = 600  # meaning 600 // 20 = 20 height per block
block_size = 30
grid_width = play_width//block_size
grid_height = play_height//block_size

top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height


# SHAPE FORMATS

S = [['..  ...',
      '......',
      '..00..',
      '.00...',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]
# index 0 - 6 represent shape


class Piece(object):
    def __init__(self, x , y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0

def create_grid(locked_positions={}):
    grid = [[(0,0,0) for _ in range(grid_width)] for _  in range(grid_height)]

    for i in range(grid_height):
        for  j in range(grid_width):
            if (j, i) in locked_positions: #in locked positions can be some -1 stats (end of game)
                grid[i][j] = locked_positions[(j,i)]
    return grid

def convert_shape_format(shape):
    positions=[]
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, colomn in enumerate(row):
            if colomn == "0":
                positions.append((shape.x+j-2, shape.y+i-2)) #offset wtf?
    return positions





def valid_space(shape, grid):

    formatted = convert_shape_format(shape)

    for pos in formatted:
        if pos[0]<0 or pos[0]>grid_width-1 or pos[1]>grid_height-1:
            return False
        elif pos[1]<0:
            pass
        elif grid[pos[1]][pos[0]] != (0,0,0):
            return False
    return True


def check_lost(positions):
    for pos in positions:
        if pos[1] < 1:
            return True
    return False

def get_shape():
    return Piece(2,-2,random.choice(shapes))

def draw_text_middle(text, size, color, surface):
    pass

def draw_grid(surface):
    sx = top_left_x
    sy = top_left_y

    for i in range(grid_height):
        pygame.draw.line(surface, (128,128,128), (sx, sy+i*block_size), (sx+play_width, sy+i*block_size))
    for j in range(grid_width):
        pygame.draw.line(surface, (128,128,128), (sx+j*block_size, sy), (sx+j*block_size, sy+play_height))


def clear_rows(grid, locked):
    pass

def draw_next_piece(surface, shape):
    font = pygame.font.SysFont('comicsans', 30)
    Label = font.render('Next Piece:', 1, (255,255,255))

    surface.blit(Label, (top_left_x+play_width+(top_left_x-Label.get_width())//2, top_left_y+play_height//2-(play_height-Label.get_height())//2))

def draw_window(surface, grid):

    surface.fill((0,0,0))

    pygame.font.init()
    font = pygame.font.SysFont("comicsans", 60)
    Label = font.render('Tetris', 1,  (255,255,255 ))

    surface.blit(Label,  (top_left_x +play_width/2-( Label.get_width()/2), 30))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
             pygame.draw.rect(surface, grid[i][j], (top_left_x+j*block_size, top_left_y+i*block_size, block_size, block_size ), 0)
    pygame.draw.rect(surface, (255,0,0), (top_left_x, top_left_y, play_width, play_height), 4)

    draw_grid(surface)

    pygame.display.update()

def main(win):

    locked_positions = {}
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.27

    while run:
        grid=create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        clock.tick()

        if fall_time//1000 > fall_speed:
            fall_time = fall_time//1000 - fall_speed
            current_piece.y+=1
            if not(valid_space(current_piece, grid)):
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                 if event.key ==  pygame.K_LEFT:
                     current_piece.x -= 1
                     if not(valid_space(current_piece, grid)):
                         current_piece.x += 1
                 if event.key ==  pygame.K_RIGHT:
                     current_piece.x += 1
                     if not(valid_space(current_piece, grid)):
                         current_piece.x -= 1
                 if event.key ==  pygame.K_DOWN:
                     current_piece.y += 1
                     if not(valid_space(current_piece, grid)):
                         current_piece.y -= 1
                 if event.key ==  pygame.K_UP:
                     current_piece.rotation += 1
                     if not(valid_space(current_piece, grid)):
                         current_piece.rotation -= 1
        shape_pos = convert_shape_format(current_piece)
        for pos in shape_pos:
            if pos[1] >= 0:
                grid[pos[1]][pos[0]] = current_piece.color
        if change_piece:
            for pos in shape_pos:
                locked_positions[pos] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False


        draw_window(win, grid)

        if check_lost(locked_positions):
            run=False
    pygame.display.quit()


def main_menu(win):
    main(win)

win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Tretris ')
main_menu(win)  # start game
