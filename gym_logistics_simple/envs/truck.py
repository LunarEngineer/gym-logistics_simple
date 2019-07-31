import random
import numpy as np
from math import sqrt, copysign
from utils import closest_node, makeName, manhattanDistance, unit_vector, angle_between
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
    if self.customer:
      print("{} is headed to service {}".format(self.name,self.customer))
      # Is there a current customer?
      # What is my next mission? RTB?
      if self.customer == "RTB":
        self.customer = self.depot
      # Now that we have a mission, where are we going?
      if self.customer == self.depot:
        location = self.depot
      else:
        location = self.customer.location
      # What edges can we move on?
      n1 = self.closest_node()
      print("{} is {} from n1 ({}) at {}".format(self.name,manhattanDistance(self.location,n1),n1,self.location))
      # In order to find out, first check to see if we are ON a node
      if manhattanDistance(self.location,n1) < 1e-3:
        # And if so, we can travel on any edge attached to that node
        n = self.nodes[n1]
        # Which node would minimize distance to the customer?
        d = [manhattanDistance(location,x) for x in n]
        n2 = n[np.argmin(d)]
        print("{} is VERY close to n1 and".format(self.name))
        # Now we have a start location (n1) and an end location (n2)
      else:
        # Otherwise we can only travel on the edge that we are ON
        # Out of the nodes attached to the closest node, which is
        #  the closest to us. This has the handy benefit of giving
        #  us the edge we are on.
        # Quickly downselect to only those nodes which share the same x or y axis
        n = [x for x in self.nodes[n1] if any([np.isclose(x,y) for x,y in zip(x,self.location)])]
        print("{} is thinking of traveling to {}".format(self.name,n))
        # Build position vectors for all of these.
        #p = [(x[0]-self.location[0],x[1]-self.location[1]) for x in n]
        # print("{} calculates position vectors to be {}".format(self.name,p))
        #p1 = (n1[0]-self.location[0],n1[1]-self.location[1])
        d = [manhattanDistance(location,x) for x in n]
        #d = [angle_between(p1,x) for x in p]
        print("{} calculates distances to be {}".format(self.name,d))
        n2 = n[np.argmin(d)]
        # Which direction is the customer in?
        direction = [x-y for x,y in zip(location,self.location)]
        print("{} sees the customer in the direction {}".format(self.name,direction))
        # Which node is in that direction? Only the first one
        #  needs to be tested because it can only be one of two.
        n1D = [x-y for x,y in zip(n1,self.location)]
        if np.dot(n1D,direction)>0:
          # If the dot product of the position vectors from the
          #  truck to n1 and from the truck to the customer
          #  happen to align then the dot product will be positive
          n2 = n1
      print("{} is {} from n2 ({})".format(self.name,manhattanDistance(self.location,n2),n2))
      # Let's do a final check for distance
      d = [manhattanDistance(self.location,x) for x in [location,n2]]
      d = d + [self.speed]
      print("{} does a sanity check on location,n2,and self.speed {} and picks {}".format(self.name,d,min(d)))
      d = min(d)
      if d > 1e-3:
        # Now there is an edge to move on defined by self.loc and n2
        e = [x-y for x,y in zip(n2,self.location)]
        print("{} will travel on edge {}".format(self.name,e))
        self.distance_traveled += d
        # Break this into X and Y components
        # normalize the distance vector
        dX,dY = d * (e/np.linalg.norm(e))    
        # EXECUTE THE MOVE ORDER!
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
          print(self.customer)
          self.fillOrder(self.customer)
        # And now that the customer is 'fulfilled', dump them!
        self.customer = None

  def getCost(self):
    return(sum([x for x in self.movement])*self.dispatch_cost)
  def getState(self):
    loc = np.array(self.location).reshape(1,2)
    sup = self.supplies.reshape(1,len(self.supplies))
    return(np.concatenate((loc,sup),axis=1))