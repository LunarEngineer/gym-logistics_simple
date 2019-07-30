import gym
import numpy as np
import pandas as pd
import random
# from Box2D.b2 import circleShape
# from igraph import Graph
from time import sleep
from gym import error, spaces, utils
from gym.utils import seeding

# Local import
from customer import Customer
from truck import Truck
from helpers import splitSquare, makeName

FPS = 50
SCALE = 30.0

VIEWPORT_W = 640
VIEWPORT_H = 480



class LogEnv(gym.Env):
  """
  This requires at least Python 3.6.
  """
  metadata = {
    'render.modes':['human', 'rgb_array'],
    'video.frames_per_second': FPS
  }

  def __init__(self,
               n: int = 20,
               r: float = 1.0,
               mapSize: float = 10.0,
               customers: int = 8,
               supply_limit: float = 100.0,
               supply_classes: int = 10,
               truck_framework: dict = None,
               seed: int = None):
    """
    Parameters
    ----------
    n : int, default 20
        Used in making a road network.
    r : float, default 1.0
        Used in making a road network.
    mapSize : float, default 10.0
        Used in making a road network.
    customers : int, default 8
        The number of customers in the network.
    supply_limit : float, default 100.0
        The total amount of supply a customer may have in any class
    supply_classes : int, default 10
        The total different 'classes' of supply.
    truck_framework : dict, default defaultTrucks
        This is a n-length dictionary of trucks with n dictionaries each
        containing 'allowed_supplies': a boolean vector of length
        supply_classes, and 'supply_limit': a float 'weight' limit.
    """
    self.seed(seed)
    self.viewer = None
    # This problem assumes an unlimited amount of supply at the depot
    self.depot = (mapSize / 2.0, mapSize / 2.0)
    self.mapSize = mapSize
    self.observation_space = spaces.Box(0.0,
                                        supply_limit,
                                        shape=(customers,2 + supply_classes),
                                        dtype=np.float32)
    # Create the road network
    self.network = self.makeRoadNetwork(n,r,mapSize)
    # This array is used in rendering
    self.lines = []
    for k in self.network.keys():
      for v in self.network[k]:
        self.lines.append((k,v))
    self.lines = list(set(map(lambda x: tuple(sorted(x)),self.lines)))
    # Create all the hungry customers
    self.customers = {}
    for _ in range(customers):
      custname = makeName()
      while custname in self.customers:
        custname = makeName()
      self.customers[custname] = Customer(self.network,
                                          supply_classes,
                                          supply_limit,
                                          greediness_mu=5./FPS,
                                          greediness_sigma=0.5/FPS,
                                          name=custname,
                                          seed=seed)
    # Create all the trucks
    if truck_framework is None:
      # This basic framework gives fuel to the tanker
      #  and not the pickups and provides one LARGE semi
      truck_framework = {
        "Snorri's Datsun":{
          "allowed_supplies": [0,1,1,1,1,1,0,1,1,1],
          "supply_limit": 500.
        },
        "Jorgen's Nissan":{
          "allowed_supplies": [0,1,1,1,1,1,0,1,1,1],
          "supply_limit": 500.
        },
        "Glinda's Tanker":{
          "allowed_supplies": [1,0,0,0,0,0,0,0,0,0],
          "supply_limit": 2000.
        },
        "Jake's Semi":{
          "allowed_supplies": [0,1,1,1,1,1,1,1,1,1],
          "supply_limit": 2000.
        }
      }
    self.trucks = {}
    for truckname in truck_framework:
      supply = truck_framework[truckname]["allowed_supplies"]
      limit = truck_framework[truckname]["supply_limit"]
      self.trucks[truckname] = Truck(nodes = self.network,
                                     depot = self.depot,
                                     supply_limit = limit,
                                     allowed_supply = supply,
                                     seed = seed,
                                     name = truckname)
    print(self.trucks)
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
     This MIGHT have to be seeded.

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
    newState = []
    reward = 0
    for customer in self.customers:
      self.customers[customer].move()
    reward = sum([self.customers[x].happiness() for x in self.customers])
    custState = np.vstack([self.customers[x].getState() for x in self.customers])
    done = reward==0
    info = {}
    # add some reward shaping for trucks....
    return(custState,reward,done,info)
    # print(custState.shape)
    # This returns state, reward, done, info
    # What *is* the state space. Each customer. That's it.

  def reset(self):
    for customer in self.customers:
      customer.reset()

  def render(self, mode='human'):
    from gym.envs.classic_control import rendering
    # Create the basic window
    world_width = self.mapSize
    scale = VIEWPORT_W/VIEWPORT_H
    # customerSize = 5.0
    
    if self.viewer is None:
      # Start the viewer
      self.viewer = rendering.Viewer(VIEWPORT_W, VIEWPORT_H)
      self.viewer.set_bounds(-2.0,12.0,-2.0,12.0)
      # Make the road lines
      for road in self.lines:
        r = rendering.Line(road[0],road[1])
        self.viewer.add_geom(r)
    for cust in self.customers:
      dot = self.viewer.draw_circle(radius=0.1)
      h = self.customers[cust].happiness()
      dot.set_color(1-h, h,.1)
      dot.add_attr(rendering.Transform(translation=self.customers[cust].location))
    return self.viewer.render(return_rgb_array = mode=='rgb_array') 


  def close(self):
    if self.viewer:
      self.viewer.close()
      self.viewer = None

  def seed(self, seed=None):
    self.np_random, seed = seeding.np_random(seed)
# class Truck():




seed = 600
a = LogEnv(seed=seed)
a.render()
for _ in range(1000):
  a.step(0)
  a.render()
  # sleep(0.001)
a.close()
print("Done")