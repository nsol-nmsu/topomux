class Topology (object):
        """
        A topology is a set of Nodes with Edges between them. This particular
        Topology class is extended to support the association of sets of
        labels and prefixes with each node, and a label to each edge.
        """

        class Node (object):
                """
                A Node within this Topology. Nodes may have a name, a set of
                labels, and a set of prefixes.
                """
                
                def __init__(self, name, labels=[], prefixes=[]):
                        """
                        Constructor for a Node.
                        """
                        self.name = name
                        self.labels = set(labels)
                        self.prefixes = set(prefixes)
                        self.edges = set([])
                
                def addLabel(self, label):
                        """ Adds a label to this Node's label set
                        """
                        self.labels |= set([label])
                
                def addPrefix(self, prefix):
                        """ Adds a prefix to this Node's prefix set
                        """
                        self.prefixes |= set([prefix])
                
                def getNeighbors(self, filter=None):
                        """ Returns a set containing the neighbors of this node
                        """
                        ret = set()
                        for edge in self.edges:
                                if filter == None or edge.label in filter:
                                        ret |= set([x for x in list(edge.pair) if x != self])
                        return ret
                
                def getDegree(self, filter=None):
                        """ Returns the number of neighbors
                        """
                        return len(self.getNeighbors(filter))
                
                def copy(self):
                        """ Returns a copy of the Node object - edges
                            will be reset
                        """
                        return Topology.Node(self.name, list(self.labels), list(self.prefixes))
                
                def __str__(self):
                        """ Returns the name of the node
                        """
                        return self.name
                
                def __repr__(self):
                        """ Returns the name of the node
                        """
                        return self.__str__()
        
        class Edge (object):
                """
                An Edge within this Topology. Edges have a capacity and delay, 
                and may have a label which classifies the edge.
                """

                def __init__(self, a, b, capacity=1000.0, delay=2.0, label=None):
                        """ Constructor
                        """
                        self.pair = set([a, b])
                        self.capacity = capacity
                        self.delay = delay
                        self.label = label
                        if a != None and b != None:
                                a.edges |= set([self])
                                b.edges |= set([self])

        def __init__(self):
                """ Constructor
                """    
                self.nodeSet = set()
                self.edgeSet = set()
        
        def copy(self):
                """ Returns a deep copy of the topology
                """
                t = Topology()
                nodeMapping = {x: x.copy() for x in self.nodeSet}
                t.nodeSet = set([x for _,x in nodeMapping.items()])
                for e in self.edgeSet:
                        i = iter(e.pair)
                        a, b = nodeMapping[next(i)], nodeMapping[next(i)]
                        t.addEdge(a, b, capacity=e.capacity, delay=e.delay, label=e.label)
                return t
        
        def findNode(self, name):
                """ Returns the node with the given name
                """
                return self.Node.get(name)
        
        def addEdge(self, a, b, **kwargs):
                """ Adds an edge between two Nodes. See the constructor of
                    Topology.Edge for details about the kwargs.
                    
                    Returns the new Edge
                """
                newEdge = self.__class__.Edge(a, b, **kwargs)
                self.edgeSet |= set([newEdge])
                return newEdge
        
        def getEdge(self, a, b):
                """ Returns the edge between nodes a and b, if it exists
                """
                return [x for x in self.edgeSet if x.pair == set([a, b])][0]
        
        def addNode(self, name=None, **kwargs):
                """ Adds a node to the graph. See the constructor of
                    Topology.Node for details about the kwargs.
                    
                    If name is None, a name will be generating using the number
                    of nodes in the nodeSet
                    
                    Returns the new Node
                """
                if name == None:
                        name = "n%d" % len(self.nodeSet)
                newNode = self.__class__.Node(name, **kwargs)
                self.nodeSet |= set([newNode])
                return newNode
        
        def getNode(self, name):
                return [x for x in self.nodeSet if x.name == name][0]
        
        def labelAllNodes(self, label):
                """ Adds the label to all nodes
                """
                for n in self.nodeSet:
                        n.addLabel(label)
        
        def prefixAllNodes(self, prefix):
                """ Adds the prefix to all nodes
                """
                for n in self.nodeSet:
                        n.addPrefix(prefix)
                
        def labelAllEdges(self, label):
                """ Assigns the label to all edges
                """
                for e in self.edgeSet:
                        e.label = label
        
        def getPrefixes(self):
                """ Returns all prefixes served by nodes within the graph
                """
                ret = set()
                for n in self.nodeSet:
                        ret |= n.prefixes
                return ret
                
        def getNodes(self):
                """ Returns the nodeSet of this graph
                """
                return self.nodeSet
        
        def getRank(self):
                """ Returns number of nodes
                """
                return len(self.nodeSet)
        
        def getMinimumSpanningTree(self):
                """ Returns a set of edges in a MST of the graph (Prim's
                    algorithm)
                """
                
                def isCandidate(mstNodes, edge):
                        """ Helper method: returns True if edge links a node
                            in mstNodes to a node not in mstNodes
                        """
                        i = iter(edge.pair)
                        a, b = next(i), next(i)
                        if a in mstNodes and not b in mstNodes:
                                return True
                        if b in mstNodes and not a in mstNodes:
                                return True
                        return False
                
                mstNodes = set([next(iter(self.nodeSet))])
                mstEdges = set([])
                while mstNodes != self.nodeSet:
                        chosenEdge = min((
                                e for e in self.edgeSet
                                if isCandidate(mstNodes, e)
                        ), key=lambda x: x.delay)
                        mstEdges |= set([chosenEdge])
                        mstNodes |= chosenEdge.pair
                return mstEdges
        
class ImportedTopology (Topology):
        """ Used to import topologies from FNSS or NetworkX. Simply copies
            the nodes and edges; does not import the data of nodes or
            edges.
        """
        
        def __init__(self, topo):
                """ Constructor.
                    topo should be a NetworkX Graph object, or some other
                    object with compatible nodes_iter and edges_iter methods
                """
                super(ImportedTopology, self).__init__()
                self._import_from(topo)
                
        def _import_from(self, topo):
                """ Imports the nodes and edges from the topo
                """
                nodemap = {}
                for node, data in topo.nodes_iter(True):
                        nodemap[node] = self.addNode(name=("n%d" % node))
                for u, v, data in topo.edges_iter(None, True):
                        self.addEdge(nodemap[u], nodemap[v])
