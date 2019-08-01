import random
import numpy as np
from math import sqrt, copysign
from gym_logistics_simple.envs.utils import closest_node, makeName
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
               greediness_sigma: float = 0.5,
               seed: int = None,
               name: str = None):
    if name:
      self.name = name
    else:
      name = makeName()
    self.target = None
    self.nodes = nodes
    self.movement = (0,0)
    self.start_location = random.choices([x for x in self.nodes])[0]
    # Limit speed for customers.
    self.speed = 0.01
    self.supply_classes = num_classes
    self.supply_limit = supply_limit
    self.supply_rate = np.random.normal(greediness_mu,greediness_sigma,size=(num_classes))
    self.reset()
  def __repr__(self):
    return("{} - {}".format(self.name,self.location))
  def reset(self):
    self.location = self.start_location
    self.supplies = np.full((self.supply_classes),0.5 * self.supply_limit)
 
  def happiness(self):
    """
    Simple linear happiness function. What proportion of supply am I missing?
    """
    return(np.sum(self.supplies) / self.supply_classes / self.supply_limit)

  def getState(self):
    loc = np.array(self.location).reshape(1,2)
    sup = self.supplies.reshape(1,self.supply_classes)
    return(np.concatenate((loc,sup),axis=1))

  def move(self):
    if not self.target:
      # Pick a node to move towards.
      # What node is the target closest to?
      curNode = closest_node(self.location,[k for k in self.nodes.keys()])
      self.target = random.choices([x for x in self.nodes[curNode]])[0]
    # If the unit has 'fuel' (the first element of supply)
    if self.supplies[0] > 0:
      # Move towards that node from current position.
      travel = [x-y for x,y in zip(self.target,self.location)]
      dX = copysign(min(abs(travel[0]),self.speed),travel[0])
      dY = copysign(min(abs(travel[1]),self.speed),travel[1])
      self.movement = (dX,dY)
      self.location = (self.location[0] + dX, self.location[1] + dY)
    # debugStr = """
    # Debug String:
    #     Customer: {}
    #     Current Location: {}
    #     Target: {}
    #     Fuel: {}
    #     Delta: {}"
    # """.format(self.name,self.location,self.target,self.supplies[0],(dX,dY))
    # print(debugStr)
    if all(np.isclose(self.location,self.target)):
      self.target = None

    for i in range(len(self.supplies)):
      self.supplies[i] = max(0, self.supplies[i] - self.supply_rate[i])
    # Burn some supplies