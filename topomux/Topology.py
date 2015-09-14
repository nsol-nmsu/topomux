
class Topology (object):

        class Node (object):
                
                nodeSet = set()
                
                def __init__(self, name=None, labels=[], prefixes=[]):
                        if name == None:
                                name = "n%d" % len(self.__class__.nodeSet)
                        self.name = name
                        self.labels = set(labels)
                        self.prefixes = set(prefixes)
                        self.edges = set([])
                        self.__class__.nodeSet |= set([self])
                
                def addLabel(self, label):
                        self.labels |= set([label])
                
                def addPrefix(self, prefix):
                        self.prefixes |= set([prefix])
                
                def getNeighbors(self, filter=None):
                        ret = set()
                        for edge in self.edges:
                                if filter == None or edge.label in filter:
                                        ret |= set([x for x in list(edge.pair) if x != self])
                        return ret
                
                def __str__(self):
                        return self.name
                
                def __repr__(self):
                        return self.__str__()
                
                @classmethod
                def get(cls, name):
                        return [x for x in cls.nodeSet if x.name == name][0]
        
        class Edge (object):
                
                edgeSet = set()
                
                def __init__(self, a, b, capacity=1000.0, delay=2.0, label=None):
                        self.pair = set([a, b])
                        self.capacity = capacity
                        self.delay = delay
                        self.label = label
                        a.edges |= set([self])
                        b.edges |= set([self])
                        self.__class__.edgeSet |= set([self])
                
                @classmethod
                def get(cls, a, b):
                        return [x for x in cls.nodeSet if x.pair == set([a, b])][0]

        def __init__(self):        
                pass
        
        def findNode(self, name):
                return self.Node.get(name)
        
        def addEdge(self, a, b, **kwargs):
                return self.Edge(a, b, **kwargs)
        
        def addNode(self, **kwargs):
                return self.Node(**kwargs)
        
        def getPrefixes(self):
                ret = set()
                for n in self.Node.nodeSet:
                        ret |= n.prefixes
                return ret
                
        def getNodes(self):
                return self.Node.nodeSet
