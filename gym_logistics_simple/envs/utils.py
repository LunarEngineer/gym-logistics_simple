from random import choice, choices
from math import copysign
import numpy as np
import heapq

class PriorityQueue():
  def __init__(self):
    self.elements = []
  def empty(self):
    return len(self.elements) == 0
  def put(self, item, priority):
    heapq.heappush(self.elements, (priority, item))
  def get(self):
    return heapq.heappop(self.elements)[1]

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
  
def makeName():
  """
  Used as a toy function to make unique names for entities
  """
  first = ['Adkuhm', 'Akadum', 'Anin', 'Anspori', 'Anvari', 'Ari', 'Aurar', 'Austi', 'Avaldur', 'Baerdal', 'Balin', 'Balskjald', 'Balthrasir', 'Bandan', 'Bangrim', 'Bardagul', 'Beldrum', 'Bendain', 'Bendan', 'Beris', 'Bhalkyl', 'Bhalmun', 'Bharrom', 'Bhelkam', 'Bilbur', 'Bjarki', 'Bofar', 'Bragi', 'Bramdahr', 'Bramdur', 'Branmand', 'Brusy', 'Brynjolvur', 'Dagur', 'Dain', 'Dalnur', 'Darmond', 'Daskjald', 'Djoni', 'Doldram', 'Dorvari', 'Draupin', 'Dufin', 'Ebdrus', 'Ebgran', 'Edmundur', 'Eiki', 'Eilivur', 'Elindur', 'Ermrig', 'Filar', 'Finn', 'Fjalin', 'Floi', 'Floki', 'Fraeg', 'Frostar', 'Fulla', 'Fundar', 'Galren', 'Galthrum', 'Gargrom', 'Garman', 'Geirfinnur', 'Geirur', 'Gimmyl', 'Gimren', 'Gisli', 'Glovari', 'Gormur', 'Graim', 'Graldor', 'Gralkyl', 'Gralram', 'Gramdahr', 'Grandrum', 'Graniggs', 'Grenbek', 'Grilmek', 'Gusti', 'Gylvia', 'Hagbarthur', 'Hallbergur', 'Hannskjald', 'Harfur', 'Harum', 'Haugin', 'Heptin', 'Hjolman', 'Hjolmor', 'Hlevari', 'Hloin', 'Horar', 'Horkahm', 'Hurram', 'Ingivald', 'Isakur', 'Ithi', 'Ithleviur', 'Jarvari', 'Jaspur', 'Jatmundur', 'Justi', 'Kari', 'Karrak', 'Kartni', 'Kiljald', 'Killin', 'Kramnom', 'Kromgrun', 'Krumgrom', 'Krumkohm', 'Leiki', 'Leivur', 'Lithri', 'Lofar', 'Lonin', 'Lonlin', 'Lonvari', 'Lythur', 'Malmun', 'Maur', 'Melnur', 'Mjothi', 'Modsognir', 'Morgus', 'Morram', 'Motar', 'Muiradin', 'Naglur', 'Nalskjald', 'Narvari', 'Nipthrasir', 'Njalur', 'Noi', 'Northrasit', 'Nyrath', 'Nyvari', 'Oddfinnur', 'Offleivur', 'Oilulvur', 'Onin', 'Onundur', 'Paitur', 'Patrin', 'Petrur', 'Ragnur', 'Ragvaldur', 'Regvari', 'Reinardun', 'Rikkin', 'Robekur', 'Roi', 'Rorin', 'Rothbar', 'Servin', 'Sigmundur', 'Sigvaldur', 'Sjurthi', 'Skafith', 'Skirfar', 'Skofti', 'Sorkvi', 'Steinfinnur', 'Steinur', 'Stigur', 'Sudri', 'Suthradir', 'Sveinur', 'Svjar', 'Taurun', 'Teitur', 'Thekkin', 'Thelron', 'Thelryl', 'Thelthrun', 'Thorar', 'Thrain', 'Throar', 'Thuldohr', 'Thulgrun', 'Thurnar', 'Thydohr', 'Thymand', 'Thymin', 'Thymur', 'Tjalvi', 'Toki', 'Toraldur', 'Torrus', 'Tyrur', 'Vagnur', 'Valbergur', 'Valdi', 'Viggar', 'Viggskjald', 'Vindalf', 'Virfi', 'Voggur', 'Yngvi', 'Aca', 'Acaida', 'Adal', 'Adeela', 'Aidura', 'Ailgiel', 'Aindina', 'Aleris', 'Alinda', 'Amara', 'Arvia', 'Baglia', 'Bagrna', 'Bamira', 'Bargun', 'Bavmorda', 'Bavola', 'Braka', 'Brana', 'Brarynn', 'Brynja', 'Cadadra', 'Cola', 'Dady', 'Dagni', 'Dagura', 'Dalvura', 'Danona', 'Darthora', 'Davia', 'Davlia', 'Defas', 'Digna', 'Digona', 'Dilgana', 'Dilura', 'Dilvina', 'Dindila', 'Dirana', 'Dirila', 'Divira', 'Dogrila', 'Dolana', 'Dondna', 'Dora', 'Dorola', 'Dothura', 'Dragrola', 'Dramola', 'Drargna', 'Drargura', 'Drathola', 'Dugrona', 'Dunora', 'Duris', 'Eloira', 'Elora', 'Eret', 'Erla', 'Estur', 'Faca', 'Fada', 'Farischa', 'Ferev', 'Fervia', 'Fidan', 'Fiden', 'Fjola', 'Frai', 'Gadona', 'Gagrila', 'Gagrlia', 'Galina', 'Gargila', 'Gaviel', 'Ghervis', 'Gimna', 'Gimona', 'Gindana', 'Gindira', 'Githlia', 'Glodona', 'Glonina', 'Glovlia', 'Gorodra', 'Gortra', 'Hanarav', 'Harinda', 'Harvia', 'Hata', 'Hatyth', 'Heden', 'Henna', 'Jaderyn', 'Japith', 'Jenka', 'Jesi', 'Jodis', 'Johild', 'Jovina', 'Justa', 'Kalady', 'Kasi', 'Kata', 'Kecha', 'Kelara', 'Kelardy', 'Kelarta', 'Kelashan', 'Kenna', 'Kezda', 'Korbeth', 'Leera', 'Legna', 'Lenora', 'Lija', 'Lilja', 'Linka', 'Lipith', 'Lirinda', 'Lirra', 'Lis', 'Loa', 'Lovisa', 'Lua', 'Mara', 'Marvia', 'Mavia', 'Meera', 'Memana', 'Micha', 'Mili', 'Mirev', 'Mireveh', 'Misi', 'Moira', 'Myagrun', 'Myalinden', 'Myanda', 'Myanra', 'Myara', 'Narta', 'Narvia', 'Naryn', 'Narynn', 'Neraeryn', 'Neralinden', 'Obara', 'Omaira', 'Quoira', 'Ragna', 'Ragnial', 'Ragriel', 'Ralvina', 'Rasicha', 'Rathila', 'Recha', 'Regna', 'Rervia', 'Ririden', 'Rishan', 'Runira', 'Rurgora', 'Ruvona', 'Ruvora', 'Saeran', 'Samara', 'Sanna', 'Sarella', 'Selah', 'Sepith', 'Serdy', 'Sexy', 'Sigga', 'Signa', 'Sigvor', 'Sishan', 'Sliryn', 'Sola', 'Tahan', 'Taleema', 'Tanda', 'Tarvia', 'Terinden', 'Terta', 'Tevia', 'Thorgiel', 'Thothila', 'Thovira', 'Tova', 'Urtha', 'Vigdis', 'Visi', 'Yngva', 'Yrsa', 'Zala', 'Zatha', 'Zazfa', 'Zerin', 'Zerun', 'Zesi']
  last = ['Axebreaker', 'Copperpot', 'Mithril-Born', 'Silverbeard', 'Blue-Mountain', 'Craghaven', 'Ironhelm', 'Craghold', 'Crannog', 'Boatmurdered', 'Alderfist', 'Ashenforge', 'Birchstone', 'Elderbear', 'Hazelaxe', 'Hollystrak', 'Junipkil', 'Oakenshield', 'Rowanagga', 'Willowgart', 'Yewhammer', 'RockRack', 'Stoneborn', 'Ironshield', 'Hammerpants', 'Ironset', 'Goldbound', 'CopperTone', 'DarkSeeker', 'ForgeKeeper', 'ShopSweeper', 'Boozebeard', 'Bunhark', "Khazad'amon", 'GoldenDwarf', 'Orcshorn', 'Hafgrey', 'Hafduergar', 'SkyLord', 'RamRider', 'GyreLord', 'FireBeard', 'SkyMiner', "Kharak'bast", 'GnarlBeard', 'QuartzEater', 'McKnuckle', 'IronJaw', 'SureFoot', 'LongWalker', 'IronSon', 'EarthChild', 'PewterSmith', 'GoldSmith', 'GunSmith', 'LeadBelly', 'GritSword', 'Goldenbrace', 'EnemyFighter', 'DirgeBane', 'Khag', 'Akurkam', 'Chazakul', 'Grimsleeper', 'Deep-Crag', 'Rockjaw', 'Highcliff', 'StoolWhoole', 'FissureFisher', 'DustBuster', 'MountainHall', 'SpiralCavern', 'Gravelgut', 'GritGobbler', 'SpireForge', 'TotalayHammard', 'MountainHome', 'KrakHammar', 'StoneShaft', 'GoldTrickle', 'Forgeworn', 'MountainHewer', 'ThunderKing', 'StormHammer', 'RiverWright', 'FrostBeard', 'HammerDasher', 'CrystalCavern', 'GoldBrewer', 'StormPeak', 'ThunderShod', 'HammerKeeper', 'WinterHill', 'Quick-Smelter', 'GoldenField', 'Red-Potter', 'Highfield', 'PoopyPants', 'HoneyWhiskey', 'BlackBone', 'LongBeard', 'SilverTome', 'MountainFall']
  firstname = choice(first)
  lastname = choice(last)
  return("{} {}".format(firstname,lastname))

def closest_node(node,nodes):
  """
  Used as a helper function in movement, finds the closest node in
  the network to another node.
  """
  nodearr = np.asarray(nodes)
  deltas = nodearr - node
  dist_2 = np.einsum('ij,ij->i', deltas, deltas)
  return tuple(nodearr[np.argmin(dist_2)])

def manhattanDistance(nodeA,nodeB):
  """
  Calculating the l1 norm, or the manhattan distance is sufficient
  for distance calculations in this environment, as all roads are
  laid out NS or EW and this *is* the distance that would have
  to be traveled.
  """
  return(sum([abs(x-y) for x,y in zip(nodeA,nodeB)]))

def makeRoadNetwork(n: int = 20,r: float = 1.0,m: float = 10.0):
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
      popInd = choices(range(len(network)),weights=wts)[0]
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
    for x1,y1 in node_dict.keys():
      # Do a little triage here and only keep four nodes on each axis,
      #  the closest to the North, South, East, and West
      NNode = None
      ENode = None
      SNode = None
      WNode = None
      for x2,y2 in node_dict[(x1,y1)]:
        if x1 == x2:
          # This is on the vertical axis.
          if y2 > y1:
            # This is to the North.
            if NNode and y2 < NNode[1]:
              NNode = (x2,y2)
            else:
              NNode = (x2,y2)
          else:
            # This is to the South.
            if SNode and y2 > SNode[1]:
              SNode = (x2,y2)
            else:
              SNode = (x2,y2)
        else:
          # This is on the horizontal axis.
          if x2 > x1:
            # This is to the East.
            if ENode and x2 < ENode[0]:
              ENode = (x2,y2)
            else:
              ENode = (x2,y2)
          else:
            # This is to the West.
            if WNode and x2 > WNode[0]:
              WNode = (x2,y2)
            else:
              WNode = (x2,y2)
      node_dict[(x1,y1)] = [x for x in [NNode,SNode,ENode,WNode] if x is not None]
    return(node_dict)

def moveOnGrid(nodes,location,target,speed):
  """
  This is used as a helper function to let trucks and customers
  use the grid road network effectively. It calls out to Dijkstras
  to calculate shortest path.
  """
  # First, run dijkstras to get the path.
  d = dijkstra(nodes,location,target)
  # The target node is the first element, though this does contain
  #  the full path in case future implementations are interested.
  n2 = d[0]
  dX, dY = [copysign(min(speed,abs(x-y)),x-y) for x,y in zip(n2,location)]
  # debugStr = """
  # Pathing from {} to {}:
  #   Dijkstra: {}
  #   N2:       {}
  #   dX,dY:    {}
  # """.format(location,target,d,n2,(dX,dY))
  # print(debugStr)
  return((dX,dY))

def cost(node1,node2):
  """
  This is used in Dijkstra's to assist in returning shortest path
  Currently this is only returning distance because in this net
  all roads are identical. This can be overloaded to change that.
  """
  return(manhattanDistance(node1,node2))

def onEdge(nodes,node):
  """
  This helper function returns the start and end nodes for the
  edge that an intermediary node is located on. 
  """
  nearNode = closest_node(node,[x for x in nodes.keys()])
  dN = [x-y for x,y in zip(node,nearNode)]
  farNodes = nodes[nearNode]
  dFar = [[y-z for y,z in zip(x,nearNode)] for x in farNodes]
  farNode = [x for x,y in zip(farNodes,dFar) if np.dot(y,dN)>0][0]
  return [nearNode, farNode]

def dijkstra(nodes,location,target):
  """
  Shamelessly borrowed from Red Blob Games.
  https://www.redblobgames.com/pathfinding/a-star/implementation.html
  """
  # Let's do *one* very small sanity check to see if the location and
  #  the target are identical. If so, just return the target.
  if manhattanDistance(location,target) < 1e-3:
    return([target])
  # One thing that needs to be preloaded is that nodes needs to be
  #  updated to include the target.
  # Add the target nodes to the network; we can clean them up when
  #  we're done. Same for start location
  targetCleanUp = False
  if not target in nodes:
    targetCleanUp = True
    targetNodes = onEdge(nodes,target)
    for node in targetNodes:
      nodes[node].append(target)
  locationCleanUp = False
  if not location in nodes:
    locationCleanUp = True
    locationNodes = onEdge(nodes,location)
    for node in locationNodes:
      nodes[node].append(location)
  if not target in nodes:
    nodes[target] = targetNodes
  if not location in nodes:
    nodes[location] = locationNodes
  #print("Nodes Target {} == Nodes Location {} : {}".format(nodes[target],nodes[location],nodes[target]==nodes[location]))
  #print("Nodes Target sort {} == Nodes Location sort {}".format(nodes[target].sort(),nodes[location].sort()))
  if len(set(nodes[target]+nodes[location]))<3:
    # Clean up
    if targetCleanUp:
      for node in targetNodes:
        nodes[node].pop()
      nodes.pop(target)
    if locationCleanUp:
      for node in locationNodes:
        nodes[node].pop()
      nodes.pop(location)
    return [(target)]
  # Now for the Dijkstra's bit
  frontier = PriorityQueue()
  frontier.put(location, 0)
  came_from = {}
  cost_so_far = {}
  came_from[location] = None
  cost_so_far[location] = 0
  # Now loop on down the line
  while not frontier.empty():
    current = frontier.get()
    if current == target:
      break
    connectedNodes = nodes[current]
    for next in nodes[current]:
      new_cost = cost_so_far[current] + cost(current,next)
      if next not in cost_so_far or new_cost < cost_so_far[next]:
        cost_so_far[next] = new_cost
        priority = new_cost
        frontier.put(next, priority)
        came_from[next] = current
  # Clean up
  if targetCleanUp:
    for node in targetNodes:
      nodes[node].pop()
    nodes.pop(target)
  if locationCleanUp:
    for node in locationNodes:
      nodes[node].pop()
    nodes.pop(location)
  # Make path
  current = target
  path = []
  while current != location:
    path.append(current)
    current = came_from[current]
  path.reverse()
  return path

def onAxis(node1,node2):
  """
  This takes two nodes as parameters and does a proximity check on
  both axes. If either the x or y axes of the nodes are 'close 
  enough' then this returns true. This is written the way it is for
  clarity, not for brevity.
  """
  xClose = np.isclose(node1[0],node2[0])
  if not xClose:
    yClose = np.isclose(node1[1],node2[1])
    return(yClose)
  else:
    return(True)
  
def displacement(farNode,nearNode):
  """
  This takes a far and near node as input and calculates a
  displacement vector
  """
  return([(x-y) for x,y in zip(farNode,nearNode)])


def testCase():
  nodes = {
    (0.0,10.0)  : [(0.0,5.0),(5.0,10.0)],
    (5.0,10.0)  : [(0.0,10.0),(5.0,7.5),(7.5,10.0)],
    (7.5,10.0)  : [(5.0,10.0),(7.5,7.5),(10.0,10.0)],
    (10.0,10.0) : [(7.5,10.0),(10.0,7.5)],
    (5.0,7.5)   : [(5.0,10.0),(7.5,7.5),(5.0,5.0)],
    (7.5,7.5)   : [(7.5,10.0),(10.0,7.5),(7.5,5.0),(5.0,7.5)],
    (10.0,7.5)  : [(10.0,10.0),(7.5,7.5),(10.0,5.0)],
    (0.0,5.0)   : [(0.0,10.0),(5.0,5.0),(0.0,0.0)],
    (5.0,5.0)   : [(0.0,5.0),(5.0,7.5),(7.5,5.0),(5.0,0.0)],
    (7.5,5.0)   : [(5.0,5.0),(7.5,7.5),(10.0,5.0)],
    (10.0,5.0)  : [(10.0,7.5),(7.5,5.0),(10.0,0.0)],
    (0.0,0.0)   : [(0.0,5.0),(5.0,0.0)],
    (5.0,0.0)   : [(0.0,0.0),(5.0,5.0),(10.0,0.0)],
    (10.0,0.0)  : [(5.0,0.0),(10.0,5.0)]
  }

  target = (9.9,7.5)
  # Test case 1: On node and far from customer
  # should head north (or east)
  location = (5.0,5.0)
  print("Test 1:")
  print("\tTarget: {}".format(target))
  print("\tLocation: {}".format(location))
  print("\tDjikstra output {}".format(dijkstra(nodes,location,target)))
  print("\tMovement Order {}".format(moveOnGrid(nodes,location,target,0.1)))
  print("\tMovement Order should be North or East")
  #moveOnGrid(nodes,location,target,0.1)

  # Test case 2: On edge and closish to customer
  # should head south
  location = (10.0,8.0)
  print("Test 2:")
  print("\tTarget: {}".format(target))
  print("\tLocation: {}".format(location))
  print("\tDjikstra output {}".format(dijkstra(nodes,location,target)))
  print("\tMovement Order {}".format(moveOnGrid(nodes,location,target,0.1)))
  print("\tMovement Order should be South")

  # Test case 3: On edge and far from customer
  # should head north
  location = (5.0,7.3)
  print("Test 3:")
  print("\tTarget: {}".format(target))
  print("\tLocation: {}".format(location))
  print("\tDjikstra output {}".format(dijkstra(nodes,location,target)))
  print("\tMovement Order {}".format(moveOnGrid(nodes,location,target,0.1)))
  print("\tMovement Order should be North")

  # Test case 4: On node and near customer
  # Should head west
  location = (10.0,7.5)
  print("Test 4:")
  print("\tTarget: {}".format(target))
  print("\tLocation: {}".format(location))
  print("\tDjikstra output {}".format(dijkstra(nodes,location,target)))
  print("\tMovement Order {}".format(moveOnGrid(nodes,location,target,0.1)))
  print("\tMovement Order should be West")

  # Test case 5: Due west of target on same edge
  location = (9.7,7.5)
  print("Test 5:")
  print("\tTarget: {}".format(target))
  print("\tLocation: {}".format(location))
  print("\tDjikstra output {}".format(dijkstra(nodes,location,target)))
  print("\tMovement Order {}".format(moveOnGrid(nodes,location,target,0.1)))
  print("\tMovement Order should be East")
