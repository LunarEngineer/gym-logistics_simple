import random
import numpy as np
from math import sqrt, copysign
from helpers import closest_node, makeName
class Truck():
  """
  A truck is an entity on the road network. They will travel
   within the road network by moving directly towards an assigned
   customer to deliver a truckload of supply. Trucks may be given
   two distinct sets of orders.
  The first order is 'fill' and is passed as a list of length n
   which sums to one. This represents the priority of goods for the
   upcoming mission.
  The second order is 'deliver' and is passed as a customer object
   which the truck can query for location.
  When a truck moves within 'kissing' distance of a customer it will
   'deliver' goods and refill the customer to the customer's limit
   for all supplies which the truck carries. A truck can, in theory,
   make multiple deliveries
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
               depot: tuple = (0.50,0.5),
               supply_limit: float = 100.0,
               allowed_supply: list = None,
               seed: int = None,
               name: str = None):
    if name:
      self.name = name
    else:
      name = makeName()

    
    self.nodes = nodes
    self.depot = depot
    self.start_location = depot
    # Limit speed for trucks.
    self.speed = 0.1
    # Supply information
    self.allowed_supply = allowed_supply
    self.supply_limit = supply_limit
    self.reset()

  def __repr__(self):
    return(" : ".join(["{} - {}".format(x,y) for x,y in zip(self.supply_priority,self.supplies)]))

  def reset(self):
    # Keep track of mileage
    self.movement = (0,0)
    self.miles_traveled = 0
    # Initial location
    self.location = self.start_location
    # Set initial supply priority
    self.supplies = [0. for n in self.allowed_supply]
    self.supply_priority = [x / sum(self.allowed_supply) for x in self.allowed_supply]
    # Clean slate for customers
    self.missions = []
    self.customer = None
    # These are used for movement tracking
    self.to_node = None
    self.from_node = None

  def refill(self):
    print('do me')
    # Are we close to home?
    # If so, fill up according to the supply priority
  def supply(self,cust):
    print("do me")
  def fillOrder(self,target):
    print("do me")

  def move(self):
    # Does the unit have a customer to service?
    if len(self.missions) > 0:
      # Is there a current customer?
      if not self.customer:
        # What is my next mission? RTB?
        if self.missions[0] == "RTB":
          self.customer = self.depot
        else:
          self.customer = self.missions[0]
      # Now that we have a mission
      if not self.from_node:
        # What is the closest node to us?
        self.from_node = closest_node(self.location,[k for k in self.nodes.keys()])
      if not self.to_node:
        # Out of the nodes that are reachable from the from_node,
        #  which is the closest to the customer? Manhattan distance
        #  is fine for this.
        if self.customer == self.depot:
          location = self.depot
        else:
          location = self.customer.location
        n = np.argmax([sum(abs(x[0]-location[0]),abs(x[1]-location[1])) for x in self.nodes[from_node]])
        self.to_node = self.nodes[from_node][n]
      # Now that there is a from node and a to node, move in the direction of the customer.
      # 



a = list()

a.append("B")
a.append("C")
print(a)
print(a[0])
print(a.pop(0))
print(a)