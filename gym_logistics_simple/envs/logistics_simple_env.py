import gym
import numpy as np
#import pandas as pd
#import random
from time import sleep
from gym import error, spaces, utils
from gym.utils import seeding

# Local import
from customer import Customer
from truck import Truck
from utils import splitSquare, makeName, makeRoadNetwork

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
               seed: int = None,
               maxSteps = 10000):
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
    self.max_step = maxSteps
    
    # Create the road network
    self.network = makeRoadNetwork(n,r,mapSize)
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
      # Costs and speed are roughly scaled to size of load
      truck_framework = {
        "Snorri's Datsun":{
          "allowed_supplies": [0,1,1,1,1,1,0,1,1,1],
          "supply_limit": 500.,
          "dispatch_cost": -2.,
          "speed": 0.1
        },
        "Jorgen's Nissan":{
          "allowed_supplies": [0,1,1,1,1,1,0,1,1,1],
          "supply_limit": 500.,
          "dispatch_cost": -2.,
          "speed": 0.1
        },
        "Glinda's Tanker":{
          "allowed_supplies": [1,0,0,0,0,0,0,0,0,0],
          "supply_limit": 2000.,
          "dispatch_cost": -10.,
          "speed": 0.05
        },
        "Jake's Semi":{
          "allowed_supplies": [0,1,1,1,1,1,1,1,1,1],
          "supply_limit": 2000.,
          "dispatch_cost": -10.,
          "speed": 0.05
        }
      }
    self.trucks = {}
    for truckname in truck_framework:
      supply = np.array(truck_framework[truckname]["allowed_supplies"])
      limit = truck_framework[truckname]["supply_limit"]
      speed = truck_framework[truckname]["speed"]
      cost = truck_framework[truckname]["dispatch_cost"]
      supply_priority = supply / sum(supply)
      self.trucks[truckname] = Truck(nodes = self.network,
                                     depot = self.depot,
                                     supply_limit = limit,
                                     allowed_supply = supply,
                                     supply_priority = supply_priority,
                                     dispatch_cost = cost,
                                     seed = seed,
                                     name = truckname)

    self.observation_space = spaces.Box(
      low = 0,
      high = np.inf,
      shape = (customers + len(truck_framework),2 + supply_classes),
      dtype = np.float16)
    self.action_space = spaces.Box(
      low = 0,
      high = customers+1,
      shape = (len(truck_framework),1 + supply_classes),
      dtype = np.uint8)
    # Start everything up
    self.reset()
  def step(self, action):
    self._take_action(action)
    self.current_step += 1
    reward = self._calculate_reward()
    obs = self._next_observation()
    done = reward==0 or self.current_step >= self.max_step
    return(obs,reward,done,{})

  def reset(self):
    self.current_step = 0
    for customer in self.customers:
      self.customers[customer].reset()
    for truck in self.trucks:
      self.trucks[truck].reset()

  def render(self, mode='human'):
    from gym.envs.classic_control import rendering
    # Create the basic window
    world_width = self.mapSize
    scale = VIEWPORT_W/VIEWPORT_H
    if self.viewer is None:
      # Start the viewer
      self.viewer = rendering.Viewer(VIEWPORT_W, VIEWPORT_H)
      self.viewer.set_bounds(-2.0,12.0,-2.0,12.0)
      # Make the road lines
      for road in self.lines:
        r = rendering.Line(road[0],road[1])
        self.viewer.add_geom(r)
      # Draw the depot
      dot = rendering.make_circle(radius=0.2,res=30,filled=True)
      dot.set_color(0,0,1)
      dot.add_attr(rendering.Transform(translation=self.depot))
      self.viewer.add_geom(dot)
    # Draw the customers
    for cust in self.customers:
      dot = self.viewer.draw_circle(radius=0.1)
      h = self.customers[cust].happiness()
      dot.set_color(1-h, h,.1)
      dot.add_attr(rendering.Transform(translation=self.customers[cust].location))
    # Draw trucks not at the depot
    for truck in self.trucks:
      if not all(np.isclose(self.depot,self.trucks[truck].location)):
        dot = self.viewer.draw_circle(radius=0.1)
        dot.set_color(0,0,1)
        dot.add_attr(rendering.Transform(translation=self.trucks[truck].location))
    return self.viewer.render(return_rgb_array = mode=='rgb_array') 

  def close(self):
    if self.viewer:
      self.viewer.close()
      self.viewer = None

  def seed(self, seed=None):
    self.np_random, seed = seeding.np_random(seed)

  def _next_observation(self):
    # I need customer status
    custState = np.vstack([self.customers[x].getState() for x in self.customers])
    # I need truck status
    truckState = np.vstack([self.trucks[x].getState() for x in self.trucks])
    obs = np.vstack([custState,truckState])
    return(obs)

  def _take_action(self,action):
    """
    Action is an n x m+1 matrix of integers. Each row is an 'order'
    to a specific truck with the first element being the customer to
    start chasing and the second through last elements the supply
    priority for this truck.

    I think that the feature space might HAVE to account explicitly
    for the allowed supply in each truck... it wouldn't be too hard
    to adjust, but it is something to keep in mind.
    """
    trucks = list(self.trucks.keys())
    customers = list(self.customers.keys())
    # Move the customers.
    for customer in self.customers:
      self.customers[customer].move()
    # Update the customer locations for the trucks.
    for i in range(len(action)):
      truck = self.trucks[trucks[i]]
      # Split apart the mission and the priority
      customer_number = action[i][0]
      supply_priority = action[i][1:]
      # Update the supply priority (it will get normalized inside)
      truck.changePriority(supply_priority)
      # Go chase the customer
      if customer_number < len(self.customers):
        truck.customer = self.customers[customers[customer_number]]
      elif customer_number == len(self.customers):
        truck.customer = "RTB"
    # debugString = """
    # Truck 1: {}
    # """.format(self.trucks[trucks[i]])
    # print(debugString)
    # Move the trucks.
    for truck in self.trucks:
      self.trucks[truck].move()

  def _calculate_reward(self):
    # At any given time the agent is rewarded for how happy their customers are
    custReward = sum([self.customers[x].happiness() for x in self.customers])
    # and penalized for how much their trucks are driving.
    truckCost = sum([self.trucks[x].getCost() for x in self.trucks])
    return(custReward + truckCost)


# Here goes a random agent
seed = 600
env = LogEnv(seed=seed)
env.render()
i = 0
done = False
truckorders = np.full((4,11),1,'uint8')

while not done and i < 1000:
  # How many trucks? 4. How many supply classes? 10.
  # How many customers? 8.
  # Actions need to be a 4x11 numpy array of uint8<9
  a = truckorders
  # print("Environment is in step: {}".format(i))
  s, r, done, _ = env.step(a)
  print(r)
  env.render()
  i+=1
  # sleep(0.1)
env.close()
print("Done")