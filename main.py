import random as rng
from config import *

rng.seed(0)

class Being():
  def __init__(self, world, x=None, y=None, size = 1):
    self.world = world
    self.x = x
    self.y = y
    self.size = size

  def get_distance(self, item):
    return ((item.x - self.x)**2 + (item.y - self. y)**2)**0.5

  def get_direction(self, item):
    distance = self.get_distance(item)
    if distance == 0:
      direction = (0, 0)
    else:
      direction = ((item.x - self.x)/distance, (item.y - self.y)/distance)
    return direction

  def __repr__(self):
    return f"{round(self.x)}, {round(self.y)}, {round(self.size, 2)}"


class Node:
  def __init__(self, x_min, x_max, y_min, y_max, parent = None):
    self.x_min = x_min
    self.x_max = x_max
    self.y_min = y_min
    self.y_max = y_max
    self.x_mid = int((self.x_max + self.x_min)/2)
    self.y_mid = int((self.y_max + self.y_min)/2)
    self.parent = parent
    if self.parent is None:
      self.depth = 0 
    else:
      self.depth = parent.depth + 1
    # step variable is set in config.py and is the minimum distance between food
    # this if statement assumes a square world. If the world is a rectangle, changes are needed
    if self.x_max - self.x_min > step:
      self.terminal = False
    else:
      self.terminal = True
    self.children = []
    self.leaf = True

  def calc_child_index(self, child):
    assert self.x_min <= child.x < self.x_max
    assert self.y_min <= child.y < self.y_max 
    
    if child.x < self.x_mid:
      if child.y < self.y_mid:
        return 0
      else:
        return 1
    else:
      if child.y < self.y_mid:
        return 2
      else:
        return 3

  def insert(self, item):
    if self.children == []:
      self.children = [item]
    else:
      if self.terminal:
        self.children.append(item)
      else:
        if self.leaf == True:
          self.leaf = False
          existing_child = self.children[0]
          self.children = [Node(self.x_min, self.x_mid, self.y_min, self.y_mid, self),
                           Node(self.x_min, self.x_mid, self.y_mid, self.y_max, self),
                           Node(self.x_mid, self.x_max, self.y_min, self.y_mid, self),
                           Node(self.x_mid, self.x_max, self.y_mid, self.y_max, self)]
          self.children[self.calc_child_index(existing_child)].insert(existing_child)
        self.children[self.calc_child_index(item)].insert(item)
  
  def search(self, x_min, y_min, x_max, y_max):  
    if self.leaf:
      if self.children is None:
        return []
      else:
        return self.children
    # the conditions are strict at the bottom end because nodes
    # may contain elements at their minimums, but not at the their maximums
    else:
      candidates = []
      for node in self.children:
        if not(x_max < node.x_min or node.x_max <= x_min):
          if not(y_max < node.y_min or node.y_max <= y_min):
            candidates.extend(node.search(x_min, y_min, x_max, y_max))
      return candidates
  
  def __repr__(self):
    if self.children == []:
      return self.depth*"  " + f"[x from {self.x_min} to {self.x_max} and y from {self.y_min} to {self.y_max}]"
    elif self.leaf:
      return self.depth*"  " + f"[x from {self.x_min} to {self.x_max} and y from {self.y_min} to {self.y_max} " + ", ".join([f"({child})" for child in self.children]) + "]"
    else:
      return self.depth*"  " + f"[x from {self.x_min} to {self.x_max} and y from {self.y_min} to {self.y_max}\n" + "\n".join([node.__repr__() for node in self.children]) + "\n" + self.depth*"  " + "]"

beings = []

for i in range(40):
  new = Being(None, rng.randint(0, width + 1), rng.randint(0, height + 1), 1.5 - rng.random())
  beings.append(new)

Tree = Node(0, width + 1, 0, height + 1)

for i in beings:
  Tree.insert(i)

print("Done")
print(Tree)

theOne = Being(None, 200, 200)

range = 50
x = 200
y = 200
# find all items within range 50 of (200, 200)
x_min = x - range
y_min = y - range
x_max = x + range
y_max = y + range

for i in Tree.search(x_min, y_min, x_max, y_max):
  print(i, theOne.get_distance(i))