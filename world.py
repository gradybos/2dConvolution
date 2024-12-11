"""
Author: Grady Bosanko
Version: Spring 2024
"""
import numpy as np
import matplotlib.pyplot as plt
import random
class World:
  
  def __init__(self, rows, cols, default_val=0):
    self.world_size = (rows, cols)
    self.world = np.full(self.world_size, default_val, np.float32)

  def set_cell(self, row, col, val):
    self.world[row][col] = val

  def get_cell_value(self, row, col):
    return self.world[row][col]

  def set_row(self, row, val):
    for col_num, col in enumerate(self.world[row]):
      self.world[row][col_num] = val

  def set_col(self, col, val):
    for row in self.world:
      row[col] = val

  def convolve(self, kernel:np.ndarray):
    '''
    convolve self with a 2D sliding window kernel
    '''
    new_world = World(self.world_size[0], self.world_size[1])

    # iterate through every row in world
    for row_num,row in enumerate(self.world):
      # iterate through every col in row
      for col_num, col in enumerate(row): # add check for corners instead of just top/bottom
        new_value = self.convolve_single_coord(kernel, (row_num, col_num))
        new_world.world[row_num][col_num] = new_value

    self.world = new_world.world

  def get_kernel_bounds(self, kernel, coords):
    kernel_start = [0,0]
    kernel_mid = len(kernel)//2
    kernel_end = [len(kernel)-1,len(kernel)-1]
    row = coords[0]
    col = coords[1]
    #left edge distance = col_num
    if col - kernel_mid < 0: # left tiles of kernel out of bounds
      kernel_start[1] = kernel_mid - col
    #right edge distance = cols - col_num - 1
    elif (self.world_size[1] - col - 1) - kernel_mid < 0: # right tiles of kernel out of bounds
      kernel_end[1] -= kernel_mid - (self.world_size[1] - col - 1)
    #top edge distance = row_num
    if row - kernel_mid < 0: # top tiles of kernel out of bounds
      kernel_start[0] = kernel_mid - row
    #bottom edge distance = rows - row_num - 1
    elif self.world_size[0] - row - 1 - kernel_mid < 0: # bottom tiles of kernel out of bounds
      kernel_end[0] -= kernel_mid - (self.world_size[0] - row - 1)
    return (kernel_start, kernel_end)

  def convolve_single_coord(self, kernel, coords):
    (kernel_start, kernel_end) = self.get_kernel_bounds(kernel, coords)
    kernel_mid = len(kernel)//2
    kernel_size = len(kernel)
    sum = 0
    kernel_rows = range(kernel_start[0], kernel_end[0] + 1)
    kernel_cols = range(kernel_start[1], kernel_end[1] + 1)
    # apply kernel as normal, but if target cell is out of bounds, use central value instead
    for row in range(kernel_size):
      for col in range(kernel_size):
        if row in kernel_rows and col in kernel_cols:
          sum += self.world[coords[0]-kernel_mid+row][coords[1]-kernel_mid+col] * kernel[row][col]
        else:
          sum += self.world[coords[0]][coords[1]] * kernel [row][col]
    return sum

  def step(self, kernel):
    self.convolve(kernel)

  def step_n_times(self, kernel, n):
    count = 0
    while count < n:
      self.convolve(kernel)
      count+=1

  def show(self, cmap_name='inferno')->None:
    '''
    Downey's code to plot a cellular array in a pretty way
    '''
    #color map
    cmap = plt.get_cmap(cmap_name)
    #plot using colormap
    plt.imshow(self.world, cmap=cmap, interpolation='none')

  def copy(self):
    copy = World(self.world_size[0], self.world_size[1])
    for row_num, row in enumerate(self.world):
      for col_num, col in enumerate(row):
        val_to_copy = self.get_cell_value(row_num, col_num)
        copy.set_cell(row_num, col_num, val_to_copy)
    return copy