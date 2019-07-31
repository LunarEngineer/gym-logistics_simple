from random import choice, choices
import numpy as np
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
  first = ['Adkuhm', 'Akadum', 'Anin', 'Anspori', 'Anvari', 'Ari', 'Aurar', 'Austi', 'Avaldur', 'Baerdal', 'Balin', 'Balskjald', 'Balthrasir', 'Bandan', 'Bangrim', 'Bardagul', 'Beldrum', 'Bendain', 'Bendan', 'Beris', 'Bhalkyl', 'Bhalmun', 'Bharrom', 'Bhelkam', 'Bilbur', 'Bjarki', 'Bofar', 'Bragi', 'Bramdahr', 'Bramdur', 'Branmand', 'Brusy', 'Brynjolvur', 'Dagur', 'Dain', 'Dalnur', 'Darmond', 'Daskjald', 'Djoni', 'Doldram', 'Dorvari', 'Draupin', 'Dufin', 'Ebdrus', 'Ebgran', 'Edmundur', 'Eiki', 'Eilivur', 'Elindur', 'Ermrig', 'Filar', 'Finn', 'Fjalin', 'Floi', 'Floki', 'Fraeg', 'Frostar', 'Fulla', 'Fundar', 'Galren', 'Galthrum', 'Gargrom', 'Garman', 'Geirfinnur', 'Geirur', 'Gimmyl', 'Gimren', 'Gisli', 'Glovari', 'Gormur', 'Graim', 'Graldor', 'Gralkyl', 'Gralram', 'Gramdahr', 'Grandrum', 'Graniggs', 'Grenbek', 'Grilmek', 'Gusti', 'Gylvia', 'Hagbarthur', 'Hallbergur', 'Hannskjald', 'Harfur', 'Harum', 'Haugin', 'Heptin', 'Hjolman', 'Hjolmor', 'Hlevari', 'Hloin', 'Horar', 'Horkahm', 'Hurram', 'Ingivald', 'Isakur', 'Ithi', 'Ithleviur', 'Jarvari', 'Jaspur', 'Jatmundur', 'Justi', 'Kari', 'Karrak', 'Kartni', 'Kiljald', 'Killin', 'Kramnom', 'Kromgrun', 'Krumgrom', 'Krumkohm', 'Leiki', 'Leivur', 'Lithri', 'Lofar', 'Lonin', 'Lonlin', 'Lonvari', 'Lythur', 'Malmun', 'Maur', 'Melnur', 'Mjothi', 'Modsognir', 'Morgus', 'Morram', 'Motar', 'Muiradin', 'Naglur', 'Nalskjald', 'Narvari', 'Nipthrasir', 'Njalur', 'Noi', 'Northrasit', 'Nyrath', 'Nyvari', 'Oddfinnur', 'Offleivur', 'Oilulvur', 'Onin', 'Onundur', 'Paitur', 'Patrin', 'Petrur', 'Ragnur', 'Ragvaldur', 'Regvari', 'Reinardun', 'Rikkin', 'Robekur', 'Roi', 'Rorin', 'Rothbar', 'Servin', 'Sigmundur', 'Sigvaldur', 'Sjurthi', 'Skafith', 'Skirfar', 'Skofti', 'Sorkvi', 'Steinfinnur', 'Steinur', 'Stigur', 'Sudri', 'Suthradir', 'Sveinur', 'Svjar', 'Taurun', 'Teitur', 'Thekkin', 'Thelron', 'Thelryl', 'Thelthrun', 'Thorar', 'Thrain', 'Throar', 'Thuldohr', 'Thulgrun', 'Thurnar', 'Thydohr', 'Thymand', 'Thymin', 'Thymur', 'Tjalvi', 'Toki', 'Toraldur', 'Torrus', 'Tyrur', 'Vagnur', 'Valbergur', 'Valdi', 'Viggar', 'Viggskjald', 'Vindalf', 'Virfi', 'Voggur', 'Yngvi', 'Aca', 'Acaida', 'Adal', 'Adeela', 'Aidura', 'Ailgiel', 'Aindina', 'Aleris', 'Alinda', 'Amara', 'Arvia', 'Baglia', 'Bagrna', 'Bamira', 'Bargun', 'Bavmorda', 'Bavola', 'Braka', 'Brana', 'Brarynn', 'Brynja', 'Cadadra', 'Cola', 'Dady', 'Dagni', 'Dagura', 'Dalvura', 'Danona', 'Darthora', 'Davia', 'Davlia', 'Defas', 'Digna', 'Digona', 'Dilgana', 'Dilura', 'Dilvina', 'Dindila', 'Dirana', 'Dirila', 'Divira', 'Dogrila', 'Dolana', 'Dondna', 'Dora', 'Dorola', 'Dothura', 'Dragrola', 'Dramola', 'Drargna', 'Drargura', 'Drathola', 'Dugrona', 'Dunora', 'Duris', 'Eloira', 'Elora', 'Eret', 'Erla', 'Estur', 'Faca', 'Fada', 'Farischa', 'Ferev', 'Fervia', 'Fidan', 'Fiden', 'Fjola', 'Frai', 'Gadona', 'Gagrila', 'Gagrlia', 'Galina', 'Gargila', 'Gaviel', 'Ghervis', 'Gimna', 'Gimona', 'Gindana', 'Gindira', 'Githlia', 'Glodona', 'Glonina', 'Glovlia', 'Gorodra', 'Gortra', 'Hanarav', 'Harinda', 'Harvia', 'Hata', 'Hatyth', 'Heden', 'Henna', 'Jaderyn', 'Japith', 'Jenka', 'Jesi', 'Jodis', 'Johild', 'Jovina', 'Justa', 'Kalady', 'Kasi', 'Kata', 'Kecha', 'Kelara', 'Kelardy', 'Kelarta', 'Kelashan', 'Kenna', 'Kezda', 'Korbeth', 'Leera', 'Legna', 'Lenora', 'Lija', 'Lilja', 'Linka', 'Lipith', 'Lirinda', 'Lirra', 'Lis', 'Loa', 'Lovisa', 'Lua', 'Mara', 'Marvia', 'Mavia', 'Meera', 'Memana', 'Micha', 'Mili', 'Mirev', 'Mireveh', 'Misi', 'Moira', 'Myagrun', 'Myalinden', 'Myanda', 'Myanra', 'Myara', 'Narta', 'Narvia', 'Naryn', 'Narynn', 'Neraeryn', 'Neralinden', 'Obara', 'Omaira', 'Quoira', 'Ragna', 'Ragnial', 'Ragriel', 'Ralvina', 'Rasicha', 'Rathila', 'Recha', 'Regna', 'Rervia', 'Ririden', 'Rishan', 'Runira', 'Rurgora', 'Ruvona', 'Ruvora', 'Saeran', 'Samara', 'Sanna', 'Sarella', 'Selah', 'Sepith', 'Serdy', 'Sexy', 'Sigga', 'Signa', 'Sigvor', 'Sishan', 'Sliryn', 'Sola', 'Tahan', 'Taleema', 'Tanda', 'Tarvia', 'Terinden', 'Terta', 'Tevia', 'Thorgiel', 'Thothila', 'Thovira', 'Tova', 'Urtha', 'Vigdis', 'Visi', 'Yngva', 'Yrsa', 'Zala', 'Zatha', 'Zazfa', 'Zerin', 'Zerun', 'Zesi']
  last = ['Axebreaker', 'Copperpot', 'Mithril-Born', 'Silverbeard', 'Blue-Mountain', 'Craghaven', 'Ironhelm', 'Craghold', 'Crannog', 'Boatmurdered', 'Alderfist', 'Ashenforge', 'Birchstone', 'Elderbear', 'Hazelaxe', 'Hollystrak', 'Junipkil', 'Oakenshield', 'Rowanagga', 'Willowgart', 'Yewhammer', 'RockRack', 'Stoneborn', 'Ironshield', 'Hammerpants', 'Ironset', 'Goldbound', 'CopperTone', 'DarkSeeker', 'ForgeKeeper', 'ShopSweeper', 'Boozebeard', 'Bunhark', "Khazad'amon", 'GoldenDwarf', 'Orcshorn', 'Hafgrey', 'Hafduergar', 'SkyLord', 'RamRider', 'GyreLord', 'FireBeard', 'SkyMiner', "Kharak'bast", 'GnarlBeard', 'QuartzEater', 'McKnuckle', 'IronJaw', 'SureFoot', 'LongWalker', 'IronSon', 'EarthChild', 'PewterSmith', 'GoldSmith', 'GunSmith', 'LeadBelly', 'GritSword', 'Goldenbrace', 'EnemyFighter', 'DirgeBane', 'Khag', 'Akurkam', 'Chazakul', 'Grimsleeper', 'Deep-Crag', 'Rockjaw', 'Highcliff', 'StoolWhoole', 'FissureFisher', 'DustBuster', 'MountainHall', 'SpiralCavern', 'Gravelgut', 'GritGobbler', 'SpireForge', 'TotalayHammard', 'MountainHome', 'KrakHammar', 'StoneShaft', 'GoldTrickle', 'Forgeworn', 'MountainHewer', 'ThunderKing', 'StormHammer', 'RiverWright', 'FrostBeard', 'HammerDasher', 'CrystalCavern', 'GoldBrewer', 'StormPeak', 'ThunderShod', 'HammerKeeper', 'WinterHill', 'Quick-Smelter', 'GoldenField', 'Red-Potter', 'Highfield', 'PoopyPants', 'HoneyWhiskey', 'BlackBone', 'LongBeard', 'SilverTome', 'MountainFall']
  firstname = choice(first)
  lastname = choice(last)
  return("{} {}".format(firstname,lastname))

def closest_node(node,nodes):
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

def makeRoadNetwork(n,r,m):
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
    return(node_dict)

def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)

def angle_between(v1, v2):
    """ Returns the angle in radians between vectors 'v1' and 'v2'::

            >>> angle_between((1, 0, 0), (0, 1, 0))
            1.5707963267948966
            >>> angle_between((1, 0, 0), (1, 0, 0))
            0.0
            >>> angle_between((1, 0, 0), (-1, 0, 0))
            3.141592653589793
    """
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))