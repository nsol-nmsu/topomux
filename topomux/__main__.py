from Topology import Topology
from IcnRoutes import IcnRoutes
from pprint import pprint

def main():
        t = Topology()
        
        a = t.addNode(name='a')
        b = t.addNode(name='b')
        c = t.addNode(name='c')
        
        t.addEdge(a, b, label="any")
        t.addEdge(b, c, label="any")
        t.addEdge(a, c, label="foo")
        
        a.addPrefix("/foo/bar")
        a.addPrefix("/bar/baz")

        r = IcnRoutes(t)
        r.restrictPrefix("/bar", ["any"])
        r.restrictPrefix("/foo", ["any", "foo"])
        
        r.calculateRoutes()
        pprint(r.hops)

main()
