import random, itertools
from Topology import Topology

def preferentialAttachment(topo_list, scalar=1.0, **kwargs):
        """
        Creates links between topologies in the topo_list. For each pair of
        topologies t1, t2 in the list a pair of nodes (a in t1), (b in t2) will
        get an edge with probability given by:
         
         (scalar/2) * (a.degree + b.degree) / (t1.numEdges + t2.numEdges)
        
        Each entry in topo_list should be a (name, topo) tuple. The name will
        be used as the prefix for the nodes in that sub-topology. This is
        necessary because two nodes in different topologies may have the same
        name, and there must be no two nodes with the same name in the final
        generated topology.
        
        Any extra kwargs provided will be passed to the addEdge function when
        inter-topology links are created.
        """
        
        # create deep copies of input topos because we will modify the nodes
        # we will also use this dict to map a topology to its prefix
        t = {x.copy(): n for n,x in topo_list}
        
        # create new empty topology, then copy nodes and edges from components
        tm = Topology()
        tm.nodeSet = set.union(*[x.nodeSet for x in t])
        tm.edgeSet = set.union(*[x.edgeSet for x in t])
        
        # add prefixes to node names
        for c in t:
                for a in c.nodeSet:
                        a.name = t[c] + "_" + a.name
        
        # returns the probability that a, b should have an edge based on the
        # degrees of a and b and total edges in t1 and t2
        def p(a, b, t1, t2):
                return scalar/2.0 * (a.getDegree() + b.getDegree()) / (len(t1.edgeSet) + len(t2.edgeSet))
        
        # add edge with probability p for each pair of nodes (a, b)
        for t1, t2 in itertools.combinations(t, 2):
                for a, b in itertools.product(t1.nodeSet, t2.nodeSet):
                        if random.random() < p(a, b, t1, t2):
                                tm.addEdge(a, b, **kwargs)
                                
        return tm
