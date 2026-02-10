import pygame
import tkinter
import random
import block

pygame.init()

def getScreenHeight():
    root = tkinter.Tk()
    HEIGHT = root.winfo_screenheight()
    root.destroy()
    return HEIGHT

HEIGHT = getScreenHeight()
WIDTH = HEIGHT // 2
GRID_HEIGHT = 20
GRID_WIDTH = 10
CELL_SIZE = HEIGHT // GRID_HEIGHT

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")

BLOCK_COLORS = {'L':(1, 186, 208), 'J':(0, 220, 61), 'S':(0, 114, 215), 'Z':(235, 0, 0), 'I':(188, 0, 224), 'O':(233, 162, 2), 'T':(223, 207, 0)}
BACKGROUND_COLOR = (0, 0, 0)
LINE_COLOR = (2, 21, 38)

BLOCK_ROTATIONS = {
    'L': [
        [(1, 0), (1, 1), (1, 2), (0, 2)],
        [(0, 1), (1, 1), (2, 1), (2, 2)],
        [(1, 0), (1, 1), (1, 2), (2, 0)],
        [(0, 1), (1, 1), (2, 1), (0, 0)]
    ],
    'O': [
        [(0, 0), (1, 0), (0, 1), (1, 1)]
    ],
    'J': [
        [(0, 0), (1, 0), (1, 1), (1, 2)],
        [(0, 0), (0, 1), (1, 0), (2, 0)],
        [(0, 0), (0, 1), (0, 2), (1, 2)],
        [(0, 1), (1, 1), (2, 1), (2, 0)]
    ],
    'T': [
        [(0, 0), (0, 1), (1, 1), (0, 2)],
        [(0, 1), (1, 1), (1, 0), (2, 1)],
        [(0, 1), (1, 0), (1, 1), (1, 2)],
        [(0, 0), (1, 0), (2, 0), (1, 1)]
    ],
    'S': [
        [(0, 1), (0, 2), (1, 0), (1, 1)],
        [(0, 0), (1, 0), (1, 1), (2, 1)]
    ],
    'Z': [
        [(0, 0), (0, 1), (1, 1), (1, 2)],
        [(0, 1), (1, 1), (1, 0), (2, 0)]
    ],
    'I': [
        [(0, 1), (1, 1), (2, 1), (3, 1)],
        [(1, 0), (1, 1), (1, 2), (1, 3)]
    ]
}

BLOCKS = ['L', 'O', 'J', 'T', 'S', 'Z', 'I']
BLOCK_TYPE = random.choice(BLOCKS)
font = pygame.font.Font(None, 50)
SCORE = 0
text = font.render(f"Score: {SCORE}", True, (255, 255, 255))

grid = block.Grid(GRID_WIDTH, GRID_HEIGHT, BLOCK_COLORS, screen, CELL_SIZE)
block = block.Block(BLOCK_ROTATIONS[BLOCK_TYPE], BLOCK_COLORS[BLOCK_TYPE], CELL_SIZE, BLOCK_TYPE, screen, grid)

def drawScreen():
    screen.fill(BACKGROUND_COLOR)
    for i in range(1, GRID_HEIGHT): pygame.draw.line(screen, LINE_COLOR, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE))
    for i in range(1, GRID_WIDTH): pygame.draw.line(screen, LINE_COLOR, (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT))
    
    text = font.render(f"Score: {SCORE}", True, (255, 255, 255))

    grid.draw()

    block.draw()

    screen.blit(text, (25, 25))

    if speed_up:
        sped_text = font.render("Sped up", True, (255, 255, 255))
        screen.blit(sped_text, (WIDTH - sped_text.get_width() - 25, HEIGHT - sped_text.get_height() - 25))


run = True
clock = pygame.time.Clock()
timer = 0
speed_up = False
while run:
    clock.tick(10)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
            elif event.key == pygame.K_e:
                block.rotate(1)
            elif event.key == pygame.K_q:
                block.rotate(-1)
            elif event.key == pygame.K_a:
                block.move(-1)
            elif event.key == pygame.K_d:
                block.move(1)
            elif event.key == pygame.K_s:
                speed_up = not speed_up
            elif event.key == pygame.K_SPACE:
                block.slam()
    drawScreen()
    if timer == 2 or speed_up:
        timer = 0
        speed_up = False
        if not block.fall():
            block.updateGrid()
            BLOCK_TYPE = random.choice(BLOCKS)
            block = block.Block(BLOCK_ROTATIONS[BLOCK_TYPE], BLOCK_COLORS[BLOCK_TYPE], CELL_SIZE, BLOCK_TYPE, screen, grid)
            if not grid.isValid(block, block.x, block.y, block.rotation):
                run = False
            SCORE = grid.checkRows(SCORE)
    else:
        timer += 1
    pygame.display.flip()

print("Game Over! Your score is:", SCORE)
pygame.quit()
