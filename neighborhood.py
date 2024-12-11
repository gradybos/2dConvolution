"""
Author: Grady Bosanko
Version: Spring 2024
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as color
import random
from world import World
class Neighborhood:

  def __init__(self, rows, cols, red_percent, blue_percent):
    self.rows = rows
    self.cols = cols
    self.kernel = np.ones((3,3), np.uint8) # initialize a 3x3 kernel
    self.empty_houses = []

    empty_percent = 100 - red_percent - blue_percent
    root_neighborhood = World(rows, cols)
    for row in range(rows):
      for col in range(cols):
        percent_roll = random.randint(0, 99)
        if percent_roll < empty_percent:
          self.empty_houses.append((row, col))
        root_neighborhood.set_cell(row, col, percent_roll)

    self.red = World(rows, cols)
    self.blue = World(rows, cols)
    for row in range(rows):
      for col in range(cols):
        seed_val = root_neighborhood.get_cell_value(row, col)
        if empty_percent < seed_val <= red_percent + empty_percent:
          self.red.set_cell(row, col, 1)
        elif red_percent + empty_percent < seed_val:
          self.blue.set_cell(row, col, 1)

  def step(self, happy_threshold):
    temp_blue = self.blue.copy()
    for row in range(self.rows):
      for col in range(self.cols):
        # convolve single red tile
        happy_val = self.red.convolve_single_coord(self.kernel, (row, col))
        if happy_val >= happy_threshold and self.red.get_cell_value(row, col) == 1:
          self.red.set_cell(row, col, 1)
        elif happy_val < happy_threshold and self.red.get_cell_value(row, col) == 1:
          empty_house = random.choice(self.empty_houses)
          self.red.set_cell(row, col, 0)
          self.empty_houses.append((row, col))
          self.red.set_cell(empty_house[0], empty_house[1], 1)
          self.empty_houses.remove(empty_house)
        # convolve single blue tile
        happy_val = self.blue.convolve_single_coord(self.kernel, (row, col))
        if happy_val >= happy_threshold and self.blue.get_cell_value(row, col) == 1:
          self.blue.set_cell(row, col, 1)
        elif happy_val < happy_threshold and self.blue.get_cell_value(row, col) == 1:
          empty_house = random.choice(self.empty_houses)
          self.blue.set_cell(row, col, 0)
          self.empty_houses.append((row, col))
          self.blue.set_cell(empty_house[0], empty_house[1], 1)
          self.empty_houses.remove(empty_house)
        # ensure houses do not overlap
        if self.red.get_cell_value(row, col) == temp_blue.get_cell_value(row, col):
          self.red.set_cell(row, col, 0)
        elif self.blue.get_cell_value(row, col) == self.red.get_cell_value(row, col):
          self.blue.set_cell(row, col, 0)

  def step_n_times(self, happy_threshold, n):
    for step in range(n):
      self.step(happy_threshold)

  def show(self):
    cmap = color.ListedColormap(['black', 'red', 'blue'])
    to_display = World(self.rows, self.cols)
    for row in range(self.rows):
      for col in range(self.cols):
        if self.red.get_cell_value(row, col) == 1:
          to_display.set_cell(row, col, 1)
        elif self.blue.get_cell_value(row, col) == 1:
          to_display.set_cell(row, col, 2)
    #plot using colormap
    plt.imshow(to_display.world, cmap=cmap, interpolation='none')