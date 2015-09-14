class IcnName (object):
        
        def __init__(self, components=[]):
                if isinstance(components, str):
                        components = components.split("/")
                        if components[0] == "":
                                components = components[1:]
                self.components = components
        
        def append(self, comp):
                self.components.append(comp)
        
        def hasPrefix(self, prefix):
                if not isinstance(prefix, IcnName):
                        prefix = IcnName(prefix)
                prefix = prefix.components[:]
                
                if len(prefix) > len(self.components):
                        return False
                
                for a, b in zip(prefix, self.components):
                        if a != b:
                                return False
                
                return True
        
        def __str__(self):
                return "/" + "/".join(self.components)
        
        def __repr__(self):
                return self.__str__()
                

class IcnRoutes (object):
        
        def __init__(self, topo):
                self.topo = topo
                self.prefixes = topo.getPrefixes()
                self.hops = {t: {p: (None, None) for p in self.prefixes} for t in topo.getNodes()}
                self.restrict = {}
        
        def restrictPrefix(self, prefix, labels):
                self.restrict[prefix] = labels
        
        def getRestriction(self, name):
                name = IcnName(name)
                for p, l in self.restrict.items():
                        if name.hasPrefix(p):
                                return l
                return None
        
        def calculateRoutes(self):
                
                # if a node serves a prefix, it can reach that prefix in zero hops
                for node in self.topo.getNodes():
                        for prefix in node.prefixes:
                                self.hops[node][prefix] = (None, 0)
                
                # visit each node and propagate its prefix to its neighbors
                change = True
                while change:
                        change = False
                        for a in self.hops:
                                for p, (face, dist) in self.hops[a].items():
                                        for b in a.getNeighbors(self.getRestriction(p)):
                                                if dist != None and (self.hops[b][p][1] == None or self.hops[b][p][1] > dist + 1):
                                                        self.hops[b][p] = (a, dist + 1)
                                                        change = True
