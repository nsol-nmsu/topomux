from topomux import Topology, ImportedTopology, IcnRoutes, TopoJoiner
from pprint import pprint
import random
import networkx as nx
import fnss.topologies as ft

def main():

        # build computation layer
        #compute = ImportedTopology(ft.datacenter.fat_tree_topology(4))
	compute = ImportedTopology(ft.simplemodels.full_mesh_topology(10))
        compute.prefixAllNodes("/direct/com")
        compute.prefixAllNodes("/overlay/com")
        compute.labelAllNodes("compute")
        compute.labelAllEdges("compute")
	
        # build aggregation layer
        aggrega = ImportedTopology(ft.randmodels.barabasi_albert_topology(64, 2, 8))
	#aggrega = ImportedTopology(ft.randmodels.barabasi_albert_topology(100, 2, 10))
        aggrega.prefixAllNodes("/direct/agg")
        aggrega.prefixAllNodes("/overlay/agg")
        aggrega.labelAllNodes("aggregate")
        aggrega.labelAllEdges("normal")
        
        # make MST edges in the aggration layer the overlay graph
        for edge in aggrega.getMinimumSpanningTree():
                edge.label = "overlay"
        
        # join the aggregation and computation layers
        joined = TopoJoiner.preferentialAttachment([
                ("com", compute, None),
                ("agg", aggrega, None),
        ], label="overlay", scalar=0.5)
        
        # create ordering of aggregation nodes based on degree
        # we will connect physical nodes to the low-degree (i.e., edge)
        # aggregate nodes
        agg_nodes = sorted([x for x in joined.nodeSet if "aggregate" in x.labels], key=lambda x: x.getDegree())
        
        # introduce physical layer
	for i in xrange(0, 100):
        #for i in xrange(0, 1000):
                # create phy node
                n = joined.addNode("phy_%d" % i, labels=["physical"])
                n.addPrefix("/overlay/phy/%s" % n.name)

                # choose agg node to connect to
                a = agg_nodes[int(pow(random.random(), 2) * len(agg_nodes))]
                joined.addEdge(n, a, label="overlay")

	# export the network topology to a file
	allnodes = joined.ExportTopology()
	      
        # compute routes
        r = IcnRoutes(joined)
        r.restrictPrefix("/direct", ["normal", "overlay"])
        r.restrictPrefix("/overlay", ["overlay"])
       
        # ensure all prefixes are reachable from all nodes
        r.calculateRoutes()
        for node, pd in r.hops.items():
                for prefix, (face, hops) in pd.items():
                        if hops == None:
                                print("%s can't reach %s" % (node, prefix))
                        #print("%s -> %s : %s : %f" % (node, prefix, face, hops))

	# export the routing tables for the nodes to a file
        r.exportroutingtables(allnodes)

main()
