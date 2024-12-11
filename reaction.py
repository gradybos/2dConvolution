"""
Author: Grady Bosanko
Version: Spring 2024
"""
import numpy as np
import matplotlib.pyplot as plt
import random
from world import World
class Reaction:

  def __init__(self, rows, cols, D_a, D_b, f, k):
    self.rows = rows
    self.cols = cols
    self.D_a = D_a
    self.D_b = D_b
    self.feed_rate = f
    self.kill_rate = k
    self.a_world = World(rows, cols, 1.0)
    self.b_world = World(rows, cols, 0.0)

  def step(self, kernel):
    new_a = self.a_world.copy()
    new_b = self.b_world.copy()
    for row in range(self.rows):
      for col in range(self.cols):
        a_grad = self.a_world.convolve_single_coord(kernel, (row, col))
        a = self.a_world.get_cell_value(row, col)
        b = self.b_world.get_cell_value(row, col)
        a += self.D_a * a_grad - a*b**2 + self.feed_rate * (1-a)
        if a > 1:
          a = 1
        elif a < 0:
          a = 0
        new_a.set_cell(row, col, a)
        b_grad = self.b_world.convolve_single_coord(kernel, (row, col))
        b += self.D_b * b_grad + a*b**2 - (self.kill_rate + self.feed_rate) * b
        if b > 1:
          b = 1
        elif b < 0:
          b = 0
        new_b.set_cell(row, col, b)
    self.a_world = new_a
    self.b_world = new_b

  def step_n_times(self, kernel, n):
    for _ in range(n):
      self.step(kernel)

  def insert_b(self, row, col, val):
    self.b_world.set_cell(row, col, val)

  def show(self):
    dif_world = World(self.rows, self.cols)
    for row in range(self.rows):
      for col in range(self.cols):
        a = self.a_world.get_cell_value(row, col)
        b = self.b_world.get_cell_value(row, col)
        dif = b - a
        dif_world.set_cell(row, col, dif)

    dif_world.show('Blues')