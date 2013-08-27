# 6.00 Problem Set 11
#
# graph.py
#
# A set of data structures to represent graphs
#

class Node(object):
   def __init__(self, name):
       self.name = str(name)
   def getName(self):
       return self.name
   def __str__(self):
       return self.name
   def __repr__(self):
      return self.name
   def __eq__(self, other):
      return self.name == other.name
   def __ne__(self, other):
      return not self.__eq__(other)

class Edge(object):
   def __init__(self, src, dest):
       self.src = src
       self.dest = dest
   def getSource(self):
       return self.src
   def getDestination(self):
       return self.dest
   def __str__(self):
       return str(self.src) + '->' + str(self.dest)

class weightedEdge(Edge):
   ##adds totalDis and outdoorDis to edge class
   def __init__(self,src,dest,totalDis,outdoorDis):
      Edge.__init__(self,src,dest)
      self.totalDis=totalDis
      self.outdoorDis=outdoorDis
   def getTotalDis(self):
      return self.totalDis
   def getOutdoorDis(self):
      return self.outdoorDis
   def __str__(self):
      return str(self.src) + '->' + str(self.dest) + ' Total Distance: ' + str(self.totalDis)+ ' Outdoor Distance: ' + str(self.outdoorDis)
   
      
 

class Digraph(object):
   """
   A directed graph
   """
   def __init__(self):
       self.nodes = set([])
       self.edges = {}
   def addNode(self, node):
       if node in self.nodes:
           raise ValueError('Duplicate node')
       else:
           self.nodes.add(node)
           self.edges[node] = []
   def addEdge(self, edge):
       src = edge.getSource()
       dest = edge.getDestination()
       if not(src in self.nodes and dest in self.nodes):
           raise ValueError('Node not in graph')
       self.edges[src].append(dest)
   def childrenOf(self, node):
       return self.edges[node]
   def hasNode(self, node):
       return node in self.nodes
   def __str__(self):
       res = ''
       for k in self.edges:
           for d in self.edges[k]:
               res = res +str(k)+ '->' + str(d)+'\n'
       return res[:-1]

class weightedDigraph(Digraph):
   ##adds modifies addEdge function of parent class digraph
   ##children of a node now contains array with dest node and distances
   def __init__(self):
      Digraph.__init__(self)
   def addEdge(self, edge):
      src = edge.getSource()
      dest = edge.getDestination()
      if not(src in self.nodes and dest in self.nodes):
         raise ValueError('Node not in graph')
      self.edges[src].append([dest,[edge.getTotalDis(),edge.getOutdoorDis()]])

class path(object):
   def __init__(self,graph,start,end,maxTotalDist,maxDistOutdoors):
      self.graph=graph
      self.start=start
      self.end=end
      self.maxTotalDist=maxTotalDist
      self.maxDistOutdoors=maxDistOutdoors
      self.shortestPath=[]
      self.parsedShortestPath=[]
      self.totalDist=2**16
      
   def computeDist(self,edgesInput):
      ##takes a list of edges returns distance out doors and total distance
      ##assumes list of edges contains a valid path from first node to end node
       totalDist=0
       disOutdoors=0
       for i in xrange(0,len(edgesInput)):
           totalDist+=edgesInput[i].getTotalDis()
           disOutdoors+=edgesInput[i].getOutdoorDis()
       return totalDist,disOutdoors

   def checkConstraint(self,edgesInput):
      totalDist, disOutdoors=self.computeDist(edgesInput)
      if (totalDist<=self.maxTotalDist) and (disOutdoors<=self.maxDistOutdoors):
         return True
      else:
         return False
      
   def findShortestPaths(self):
   ##returns list of lists weighted edges each with a valid path from start to end in digraph
      self.findPathRec(self.start,[])

   def findPathRec(self,presentNode,nodeList):
    ##print 'made a recursive call'
    children=self.graph.childrenOf(presentNode)
    ##print foo
    ##print 'children length: ' + str(len(foo))
    for i in xrange(0,len(children)):
        ##print 'iteration: ' + str(i)
        newNodeList=list(nodeList)
        newNodeList.append(weightedEdge(presentNode,children[i][0],children[i][1][0],children[i][1][1]))
        ##print temp
        for j in xrange(0,len(newNodeList)):
            if (newNodeList[j].getSource()==children[i][0]):
                print 'found a loop'
                return None

        if (children[i][0]==self.end):
            print 'found the end'
            
            if self.checkConstraint(newNodeList):
               print 'passes constraint'
               totalDist,disOutdoors=self.computeDist(newNodeList)
               if totalDist<self.totalDist:
                  print 'found new shortest path'
                  self.shortestPath=newNodeList
                  self.totalDist=totalDist
            ##print 'total dis: ' + str(totalDist)
            ##for k in xrange(0,len(newNodeList)):
            ##    print newNodeList[k]
            ##return None
        else:
           print 'making recursize call'
           self.findPathRec(children[i][0],newNodeList)
        return None

   def printShortestPath(self):
      for k in xrange(0,len(self.shortestPath)):
         print str(self.shortestPath[k].getSource())

   def parseShortestPath(self):
      self.printShortestPath()
      for i in xrange(0,len(self.shortestPath)):
         self.parsedShortestPath.append(self.shortestPath[i].getSource())
      self.parsedShortestPath.append(self.shortestPath[len(self.shortestPath)-1].getDestination())
      return self.parsedShortestPath
                      
   
    
