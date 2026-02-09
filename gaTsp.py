import math
import random


class Node:
   x = None
   y = None
   
   def __init__(self, x=None, y=None):
      self.x = None
      self.y = None
      if x:
         self.x = x
      if y:
         self.y = y
   def getX(self):
      return self.x
   def getY(self):
      return self.y

   def meanDistance(self, node):
      xDist = abs(self.getX() - node.getX())
      yDist = abs(self.getY() - node.getY())
      meanDist = math.sqrt( (xDist*xDist) + (yDist*yDist) )
      return meanDist
   
   def __repr__(self):
      return str(self.getX()) + ", " + str(self.getY())


class routeMngr:
   destNode = []
                 
   
   
   def getNode(self, index):
      return self.destNode[index]
   
   def nodeCount(self):
      return len(self.destNode)
   
   def adNode(self, node):
      self.destNode.append(node)

class Route:
   routemngr = None
   distance = 0
   fitness = 0.0
   route = []
   
   def __init__(self, routemngr, route=None):
      self.routemngr = routemngr
      self.fitness = 0.0
      self.distance = 0
      self.route = []
      if route:
         self.route = route
      else:
         for i in range(0, self.routemngr.nodeCount()):
            self.route.append(None)
   
   def __len__(self):
      return len(self.route)
   
   def __getitem__(self, index):
      return self.route[index]
   
   def __setitem__(self, key, value):
      self.route[key] = value
   
   def __repr__(self):
      geneString = "|"
      for i in range(0, self.routeSize()):
         geneString += str(self.getNode(i)) + "|"
      return geneString
   
   def chromosome(self):
      for NodeIndex in range(0, self.routemngr.nodeCount()):
         self.setNode(NodeIndex, self.routemngr.getNode(NodeIndex))
      random.shuffle(self.route)
   
   def getNode(self, routePosition):
      return self.route[routePosition]
   
   def setNode(self, routePosition, node):
      self.route[routePosition] = node
      self.fitness = 0.0
      self.distance = 0
   
   def getFitness(self):
      if self.fitness == 0:
         self.fitness = 1/float(self.getDistance())
      return self.fitness
   
   def getDistance(self):
      if self.distance == 0:
         routeDistance = 0
         for NodeIndex in range(0, self.routeSize()):
            fromNode = self.getNode(NodeIndex)
            destinationNode = None
            if NodeIndex+1 < self.routeSize():
               destinationNode = self.getNode(NodeIndex+1)
            else:
               destinationNode = self.getNode(0)
            routeDistance += fromNode.meanDistance(destinationNode)
         self.distance = routeDistance
      return self.distance
   
   def routeSize(self):
      return len(self.route)
   
   def containsNode(self, node):
      return node in self.route


class matePool:
   routes = []
   
   def __init__(self, routemngr, poolSize, initialise):
      self.routes = []
      for i in range(0, poolSize):
         self.routes.append(None)
      
      if initialise:
         for i in range(0, poolSize):
            newRoute = Route(routemngr)
            newRoute.chromosome()
            self.saveRoute(i, newRoute)
      
   def __setitem__(self, key, value):
      self.routes[key] = value
   
   def __getitem__(self, index):
      return self.routes[index]
   
   def getRoute(self, index):
      return self.routes[index]
  
   def saveRoute(self, index, route):
      self.routes[index] = route 
   
   def bestFit(self):
      fittest = self.routes[0]
      for i in range(0, self.poolSize()):
         if fittest.getFitness() <= self.getRoute(i).getFitness():
            fittest = self.getRoute(i)
      return fittest
   
   def poolSize(self):
      return len(self.routes)


class geneticAlgorithm:
   routemngr = None
   mutateValue = 0.015
   selectionSize  = 5
   elitism = True
   
   def __init__(self, routemngr):
      self.routemngr = routemngr
      self.mutateValue = 0.015
      self.selectionSize = 5
      self.elitism = True
   
   def survivorSlection(self, pop):
      newMattingPool = matePool(self.routemngr, pop.poolSize(), False)
      elitismOffset = 0
      if self.elitism:
         newMattingPool.saveRoute(0, pop.bestFit())
         elitismOffset = 1
      
      for i in range(elitismOffset, newMattingPool.poolSize()):
         parent1 = self.tournaSlection(pop)
         parent2 = self.tournaSlection(pop)
         child = self.OnePcross(parent1, parent2)
         newMattingPool.saveRoute(i, child)
      
      for i in range(elitismOffset, newMattingPool.poolSize()):
         self.swapMutation(newMattingPool.getRoute(i))
      
      return newMattingPool
   
   def OnePcross(self, parent1, parent2):
      child = Route(self.routemngr)
      
      startPnt = int(random.random() * parent1.routeSize())
      endPnt = int(random.random() * parent1.routeSize())
      
      for i in range(0, child.routeSize()):
         if startPnt < endPnt and i > startPnt and i < endPnt:
            child.setNode(i, parent1.getNode(i))
         elif startPnt > endPnt:
            if not (i < startPnt and i > endPnt):
               child.setNode(i, parent1.getNode(i))
      
      for i in range(0, parent2.routeSize()):
         if not child.containsNode(parent2.getNode(i)):
            for z in range(0, child.routeSize()):
               if child.getNode(z) == None:
                  child.setNode(z, parent2.getNode(i))
                  break
      
      return child
   
   def swapMutation(self, route):
      for routePos1 in range(0, route.routeSize()):
         if random.random() < self.mutateValue:
            routePos2 = int(route.routeSize() * random.random())
            
            node1 = route.getNode(routePos1)
            node2 = route.getNode(routePos2)
            
            route.setNode(routePos2, node1)
            route.setNode(routePos1, node2)
   
   def tournaSlection(self, pop):
      tournmnt = matePool(self.routemngr, self.selectionSize, False)
      for i in range(0, self.selectionSize):
         randomId = int(random.random() * pop.poolSize())
         tournmnt.saveRoute(i, pop.getRoute(randomId))
      fittest = tournmnt.bestFit()
      return fittest

   def linearRank(self,pop):
       return None


if __name__ == '__main__':
   

   fileOne='TSP1.txt'
   fileTwo='TSP2.txt'

   
   routemngr = routeMngr()
      
   def readfile():
       count=0
       #Enter File Name here fileOne , fileTwo 
       with open(fileOne) as f:
            for line in f:
               numbers_float = list(map(float, line.split()))
               #print (*numbers_float)
               count=count+1
               print(count)
               print (numbers_float[0],numbers_float[1])
               node=Node(numbers_float[0],numbers_float[1])
               routemngr.adNode(node)
                    
   readfile()
   
   # Initialize matePool
   pop = matePool(routemngr, 50, True);
   print ("Initial distance between Nodes: " + str(pop.bestFit().getDistance()))
   
   # Evolve matePool for 50 generations
   geneticAlgo = geneticAlgorithm(routemngr)
   pop = geneticAlgo.survivorSlection(pop)
   for i in range(0, 50):
      pop = geneticAlgo.survivorSlection(pop)
   
   # Printing results
   print ("Finished Calculating Optimul Route")
   print ("Final Route distance: " + str(pop.bestFit().getDistance()))
   print ("Node Visiting Solution:")
   print (pop.bestFit())
   