import random
import numpy as np
from math import sqrt, copysign
from gym_logistics_simple.envs.utils import moveOnGrid, makeName, manhattanDistance
#closest_node, makeName, manhattanDistance, unit_vector, angle_between
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
               allowed_supply: list = np.ones(10),
               supply_priority: list = np.full((10),0.1),
               speed: float = 0.1,
               dispatch_cost: float = -1,
               seed: int = None,
               name: str = None):
    if name:
      self.name = name
    else:
      name = makeName()

    self.nodes = nodes
    self.depot = depot
    self.start_location = depot
    self.speed = speed
    # Supply information
    self.supply_limit = supply_limit
    self.allowed_supply = np.array(allowed_supply)
    self.initial_supply_priority = supply_priority
    self.dispatch_cost = dispatch_cost
    # debugStr = """
    # Truck: {}
    #   Initialized with
    #   Supply limit:    {}
    #   Allowed supply:  {}
    #   Supply Priority: {}
    #   Speed:           {}
    #   Dispatch Cost:   {}
    # """.format(self.name,self.supply_limit,self.allowed_supply,self.initial_supply_priority,self.speed,self.dispatch_cost)
    # print(debugStr)
    self.reset()

  def __repr__(self):
    selfStr = """
    Truck: {}
      Supplies: {}
      Priority: {}
      Location: {}
    """.format(self.name,self.supplies,self.supply_priority,self.location)
    return(selfStr)

  def closest_node(self):
    return(closest_node(self.location,[k for k in self.nodes.keys()]))
  def reset(self):
    # Keep track of mileage
    self.movement = (0,0)
    self.distance_traveled = 0
    # Initial location
    self.location = self.start_location
    # Set the supply priority to the initial priority
    self.changePriority(self.initial_supply_priority)
    # Fill the truck to start
    self.refill()
    # Clean slate for customers
    self.mission = None
    self.customer = None
    # These are used for movement tracking
    # self.to_node = None
    # self.from_node = None

  def refill(self):
    # Draw supplies according to the supply priority.
    self.supplies = np.array([x*y*self.supply_limit for x,y in zip(self.allowed_supply,self.supply_priority)])

  def changePriority(self,priority):
    """
    This is called when an agent executes an action and updates the
    supply priority for a single truck. This is used in real life to
    fill a truck entirely with cigarettes, for example. There is NO
    check to ensure an agent doesn't set a high priority for food
    if the vehicle is a fuel tanker. The agent just won't be highly
    rewarded because the tanker cannot fulfill any needs. The only
    checking that is done here is to ensure that this is a unit
    vector.
    """
    self.supply_priority = np.array(priority / sum(priority))

  def fillOrder(self,customer):
    """
    A customer has a supply limit for every supply they *could* have
    Customers in this environment are *greedy* and will take
    everything they can to fill up to their supply limit.
    A customer is a customer object and therefore customer
    supplies is a numpy array
    """
    # What supplies does the customer need?
    customer_deficit = customer.supply_limit - customer.supplies
    # This is, in effect, bitmasking to only the supplies which
    #  the truck is allowed to carry.
    customer_request = customer_deficit * self.allowed_supply
    # Start an empty array
    customer_supplied = np.zeros(len(customer_request))
    for i in range(len(customer_supplied)):
      # and for each supply class check
      if customer_request[i] > self.supplies[i]:
        # if the customer is asking for more than the truck can give
        # and if so limit them to reality.
        customer_supplied[i] = self.supplies[i]
      else:
        # otherwise give them what they ask for.
        customer_supplied[i] = customer_request[i]
    # Update the trucks supplies appropriately.
    self.supplies -= customer_supplied
    # Update the customers supplies appropriately.
    customer.supplies += customer_supplied


  def move(self):
    """
    A customer is passed to the truck and the truck blindly pursues
    """
    self.movement = (0,0)
    debug = False
    if self.customer:
      
      # Is there a current customer?
      # What is my next mission? RTB?
      if self.customer == "RTB":
        self.customer = self.depot
      # Now that we have a mission, where are we going?
      if self.customer == self.depot:
        location = self.depot
      else:
        location = self.customer.location
      dX,dY = moveOnGrid(self.nodes,self.location,location,self.speed)
      self.movement = (dX,dY)
      self.location = (self.location[0] + dX, self.location[1] + dY)
      # Am I within kissing distance of my customer after moving?
      if manhattanDistance(self.location,location) < 1e-3:
        # Is my mission to RTB?
        if self.customer == "RTB":
          # If so, refuel / restock.
          self.refill()
          # Reset the odometer!
          self.distance_traveled = 0
        # Otherwise
        else:
          if debug:
            print(self.customer)
          self.fillOrder(self.customer)
        # And now that the customer is 'fulfilled', dump them!
        self.customer = None

  def getCost(self):
    # debugStr = """
    # Movement is {} and dispatch cost is {}
    # """.format(self.movement,self.dispatch_cost)
    # print(debugStr)
    return(sum([abs(x) for x in self.movement])*self.dispatch_cost)
  def getState(self):
    loc = np.array(self.location).reshape(1,2)
    sup = self.supplies.reshape(1,len(self.supplies))
    return(np.concatenate((loc,sup),axis=1))