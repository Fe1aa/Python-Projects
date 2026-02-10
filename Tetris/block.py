import numpy as np
import pygame
import random

class Grid:
  def __init__(self, width, height, colors, screen, cell_size):
    self.width = width
    self.height = height
    self.grid = np.array([[None for _ in range(width)] for _ in range(height)])
    self.colors = colors
    self.screen = screen
    self.cell_size = cell_size

  def isValid(self, block, new_x, new_y, new_rotation):
    for dx, dy in block.rotations[new_rotation]:
      nx = new_x + dx
      ny = new_y + dy 

      if not (0 <= nx < self.height and 0 <= ny < self.width):
        return False
      elif self.grid[nx][ny] is not None:
        return False
      
    return True
  
  def clearRow(self, row):
    for i in range(row, 0, -1):
      self.grid[i] = self.grid[i - 1]
    self.grid[0] = [None for _ in range(self.width)]

  def checkRows(self, score):
    full_rows = []
    for i in range(self.height):
      if all(cell is not None for cell in self.grid[i]):
        full_rows.append(i)
    full_rows.sort(reverse=True)
    for row in full_rows:
      self.clearRow(row)
    count = len(full_rows)
    if count == 4:
      return score + 800
    elif count == 3:
      return score + 500
    elif count == 2:
      return score + 300
    elif count == 1:
      return score + 100
    return score

  
  def update(self, block):
    for dx, dy in block.rotations[block.rotation]:
      nx = dx + block.x
      ny = dy + block.y
      self.grid[nx][ny] = block.type

  def draw(self):
    for i in range(self.height):
      for j in range(self.width):
        cell = self.grid[i][j]
        if cell is not None:
          pygame.draw.rect(self.screen, self.colors[cell], (j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size), 1)
    

class Block:
  def __init__(self, rotations, color, cell_size, _type, screen: pygame.Surface, grid: Grid):
    self.color = color
    self.x = 0
    self.y = 4
    self.rotation = random.randint(0, len(rotations) - 1)
    self.rotations = rotations
    self.cell_size = cell_size
    self.type = _type
    self.screen = screen
    self.grid = grid

  def fall(self):
    if self.grid.isValid(self, self.x + 1, self.y, self.rotation):
      self.x += 1
      return True
    return False

  def move(self, direction):
    new_y = self.y + direction
    if self.grid.isValid(self, self.x, new_y, self.rotation):
      self.y = new_y
      return True
    return False

  def rotate(self, direction):
    new_rotation = self.rotation + direction
    if new_rotation > len(self.rotations) - 1:
      new_rotation = 0
    elif new_rotation < 0:
      new_rotation = len(self.rotations) - 1

    if self.grid.isValid(self, self.x, self.y, new_rotation):
      self.rotation = new_rotation
      return True
    return False

  def slam(self):
    while(self.fall()):
      continue

  def updateGrid(self):
    self.grid.update(self)


  def draw(self):
    for dx, dy in self.rotations[self.rotation]:
      nx = (self.x + dx) * self.cell_size
      ny = (self.y + dy) * self.cell_size

      pygame.draw.rect(self.screen, self.color, (ny, nx, self.cell_size, self.cell_size), 1)

  
