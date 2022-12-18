"""
Simple routing functions for graphs
"""

from copy import copy

class Node:
    def __init__(self, name, edges):
        self.name = name
        self.edges = edges

    def __repr__(self):
        return (
            f"Node(name='{self.name}', edges={[edge.name for edge in self.edges]})")


def leasthops(srclist, destlist):
    """
    Returns the smallest number of hops between two 'clouds' of nodelistcopy in a graph.
    """
    srchops, desthops = 0, 0                                # length of src and dest trees
    srcset, destset = set(srclist), set(destlist)           # all nodelistcopy seen so far
    newsrcset, newdestset = set(srclist), set(destlist)     # nodelistcopy found during last iteration
    if newsrcset.intersection(newdestset):
        return 0
    else:
        while True:
            # try new source nodelistcopy
            trysrcset = newsrcset
            newsrcset = set()
            srchops += 1
            for node in trysrcset:
                for edge in node.edges:
                    if edge not in srcset:
                        # not in exsiting source tree
                        if edge in destset:
                            # trees have met
                            return srchops + desthops
                        else:
                            srcset.add(edge)
                            newsrcset.add(edge)
            # try new dest nodelistcopy
            trydestset = newdestset
            newdestset = set()
            desthops += 1
            for node in trydestset:
                for edge in node.edges:
                    if edge not in destset:
                        # not in existing dest tree
                        if edge in srcset:
                            # trees have met
                            return srchops + desthops
                        else:
                            destset.add(edge)
                            newdestset.add(edge)


def hoptable(nodelist):
    """Takes a list of nodes, returns a dictionary of the smallest hop distances between each pair."""
    table = {}
    nodelistcopy = copy(nodelist)
    while nodelistcopy:
        src = nodelistcopy.pop()
        table[(src, src)] = 0
        for dest in nodelistcopy:
            hops = leasthops([src], [dest])
            table[(src, dest)] = hops
            table[(dest, src)] = hops
    return table


def showhoptable(hoptable):
    valves = sorted(list(set([src for src, dest in hoptable.keys()])), key=lambda x: x.name)
    for dest in valves:
        print(f'\t{dest.name}', end='')
    for src in valves:
        print(f'\n{src.name}\t', end='')
        for dest in valves:
            print(f'{hoptable[(src, dest)]}\t', end='')
    print()