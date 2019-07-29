import gym
import numpy as np
import random
from Box2D.b2 import circleShape
from igraph import Graph
from gym import error, spaces, utils
from gym.utils import seeding
from math import sqrt

FPS = 50
SCALE = 30.0

VIEWPORT_W = 600
VIEWPORT_H = 400

class LogEnv(gym.Env):
  """
  This requires at least Python 3.6.
  """
  metadata = {'render.modes':['human']}

  def __init__(self, n: int = 20, r: float = 1.0, mapSize: float = 10.0):
    """
    Parameters
    ----------
    n : int, default 20
        Used in making a road network.
    r : float, default 1.0
        Used in making a road network.
    mapSize : float, default 10.0
        Used in making a road network.
    """
    ################################################################
    # Create the road network. This creates a dictionary keyed by
    #  (X,Y) coordinate of the node in question with each element
    #  a list of connected nodes.
    #  e.g {(NodeA):[NodeB,...,NodeZ]}
    ################################################################
    self.network = makeRoadNetwork(n,r,mapSize)
    # I need a number of customers and a logistics hub
  def makeRoadNetwork(self,n,r,m):
    """ Creates a road network for the logistics environment

    Quadtree: https://www.davideisenstat.com/cv/Eisenstat11.pdf
    Note that this is my interpretation of his method and 
     could be wrong. He is not clear in what the subscripts are
     intended to be though my interpretation is that for the
     formula $Pr(Split_n = v | Leaves_n)\defined\frac{r^|v|}{\sum_{w\inLeaves_n}r^|w|}$
     v is the depth of that particular node while w is *also* the
     depth of that particular node. This is simply a weighted
     probability distribution that more strongly weights deeply
     nested nodes.

    Parameters
    ----------
    n : int, default 20
        The number of new intersections to be added. (i.e.)
        the number of times the unit square is split beyond
        the first time.
    r : float, default 1.0
        A parameter used to force the tree to favor grids of
        a certain size. r < 1 favors big squares, r > 1 favors
        small squares, r = 1 is uniform.
    m : float, default 10.0
        This is used to define the extent of the created map

    Returns
    dict
        a dictionary of nodes with connecting nodes keyed by node
        coordinates
    -------
    """
    # Each node in this network is a subordinate square
    # Each square is initially represented by 
    # [Depth, xmin, xmax, ymin, ymax]
    #  and there is initially a square of four squares.
    # Initially there are 9 nodes. Every split adds 5 nodes.
    network = list([[1, 0.0, 0.5 * m, 0.5 * m, 1.0 * m],
                    [1, 0.5 * m, 1.0 * m, 0.5 * m, 1.0 * m],
                    [1, 0.0, 0.5 * m, 0.0, 0.5 * m],
                    [1, 0.5 * m, 1.0 * m, 0.0, 0.5 * m]])
    probs = [r**x[0] for x in network]
    while len(network) < n:
      # Every split adds 5 intersections
      wts = [r**x[0] for x in network]
      popInd = random.choices(range(len(network)),weights=wts)[0]
      subBoxes = splitSquare(network.pop(popInd))
      network += subBoxes
    node_dict = {}
    for i in range(len(network)):
      # Every corner of this square is an intersection / node
      # Southwest corner
      SW = (network[i][1],network[i][3])
      # Southeast corner
      SE = (network[i][2],network[i][3])
      # Northwest corner
      NW = (network[i][1],network[i][4])
      # Northeast corner
      NE = (network[i][2],network[i][4])
      connected = {SW:[NW,SE],
                   SE:[NE,SW],
                   NW:[NE,SW],
                   NE:[NW,SE]}
      for corner in [SW,SE,NW,NE]:
        for other_corner in connected[corner]:
          if corner in node_dict:
            if other_corner not in node_dict[corner]:
              node_dict[corner].append(other_corner)
          else:
            node_dict[corner] = [other_corner]
    return(node_dict)

  def step(self, action):

  def reset(self):

  def render(self, mode='human'):

  def close(self):

class Truck():

class Customer():
  """
  A customer is an entity on the road network. They will travel
   within the road network 'randomly' by selecting a destination
   node at random from those that are connected to a current node
   by edges. They are mindless automatons.
  Customers have a bank of supplies which they will slowly drain
   over time. The 'greediness' of each customer specifies how
   quickly they will drain their resources. Each supply starts
   full (at 100) and then each time step that a customer is 'alive'
   will drain by the greediness level. The default supply limit is
   100, but can be changed to emulate less well supplied customers.
  Supply classes:
   Class  1: Food
   Class  2: Clothing
   Class  3: Fuel
   Class  4: Building Material
   Class  5: Ammunition
   Class  6: Fun supplies
   Class  7: Large items
   Class  8: Medical Supplies
   Class  9: Repair items
   Class 10: Miscellaneous
  """
  def __init__(self,
               nodes: dict,
               num_classes: int = 10,
               supply_limit: float = 100.0,
               greediness_mu: float = 1.0,
               greediness_sigma: float = 0.5
               ):
    self.target = None
    self.nodes = nodes
    self.location = random.choices([x for x in self.nodes])[0]
    # Limit speed for customers.
    self.speed = 0.01
    self.supply_classes = num_classes
    self.supply_limit = supply_limit
    self.supplies = np.full((num_classes),0.5 * supply_limit)
    self.supply_rate = np.random.normal(greediness_mu,greediness_sigma,size=(num_classes))
  
  def happiness(self):
    """
    Simple linear happiness function. What proportion of supply am I missing?
    """
    return(np.sum(self.supplies) / self.supply_classes / self.supply_limit)

  def move(self):
    if not self.target:
      # Pick a node to move towards.
      self.target = random.choices([x for x in self.nodes[self.location]])[0]
    # If the unit has 'fuel' (the first element of supply)
    if self.supplies[0] > 0:
      # Move towards that node from current position.
      travel = [x-y for x,y in zip(self.target,self.location)]
      if travel[0] > 0:
        # Need to traverse on the x.
        dX = min(travel[0],self.speed)
      if travel[1] > 0:
        # Need to traverse on the y.
        dY = min(travel[1],self.speed)
      self.location = (self.location[0] + dX, self.location[1] + dY)
      # Decrement fuel for traveling.
      self.supplies[0] -= sqrt(dX**2 + dY**2) * 10
    # Check to see if that node is reached and if so unassign the target.
    if all(np.isclose(self.location,self.target)):
      self.target = None

def splitSquare(x):
  """
  Given a simple square x of depth x[0] (int)
  and an array of X,Y coordinates of
  x[1] = x minimum
  x[2] = x maximum
  x[3] = y minimum
  x[4] = y maximum
  create an array of four new squares as NW,NE,SW,SE
  from an even subdivision of the original square
  with depth += 1.
  This is intended to be used inside the quadtree implementation
  used when making a logistics environment.
  """
  d = x[0]
  d += 1
  xmin = x[1]
  xmax = x[2]
  ymin = x[3]
  ymax = x[4]
  NW = [d, xmin, xmin+(xmax-xmin)/2.0, ymin+(ymax-ymin)/2.0, ymax]
  NE = [d, xmin+(xmax-xmin)/2.0, xmax, ymin+(ymax-ymin)/2.0, ymax]
  SW = [d, xmin, xmin+(xmax-xmin)/2.0, ymin, ymin+(ymax-ymin)/2.0]
  SE = [d, xmin+(xmax-xmin)/2.0, xmax, ymin, ymin+(ymax-ymin)/2.0]
  out = list([NW,NE,SW,SE])
  return(out)

