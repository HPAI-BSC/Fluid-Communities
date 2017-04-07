# -*- coding: utf-8 -*-
#    Copyright (C) 2017
#    All rights reserved.
#    BSD license.
"""Asynchronous fluid communities algorithms for community detection."""

from collections import Counter
import random

__all__ = ['asyn_fluid_communities']

# Optional to fix the random seed
#random.seed(123)

def asyn_flp_3(G, k, max_iter=15):
    """
    Fluid Communities algorithm. A community detection algorithm.
    Args:
        - G: Graph to run the algorithm into.
            + type: networkx.Graph
        - k: Number of communities to search.
            + type: int
        - max_iter: Number of maximum iterations allowed.
            + type: int
    Return:
        - List of communities, where each community is a list of vertex ID.
          Each vertex ID can be either an int or str.
            + type: list(list(int or str))
    """
    # Initialization
    max_density = 1.0
    vertices = list(G)
    random.shuffle(vertices)
    communities = {n: i for i, n in enumerate(vertices[:k])}
    density = {}
    com_to_numvertices = {}
    for vertex in communities.keys():
        com_to_numvertices[communities[vertex]] = 1
        density[communities[vertex]] = max_density
    # Set up control variables and start iterating
    iter_count = 0
    cont = True
    while cont:
        cont = False
        iter_count += 1
		# Loop over all vertices in graph in a random order
        vertices = list(G)
        random.shuffle(vertices)
        for vertex in vertices:
            # Updating rule
            com_counter = Counter()
            # Take into account self vertex community
            try:
                com_counter.update({communities[vertex]: max_density / com_to_numvertices[communities[vertex]]})
            except KeyError:
                pass
            # Gather neighbour vertex communities
            for v in G[vertex]:
                try:
                    com_counter.update({communities[v]: max_density / com_to_numvertices[communities[v]]})
                except KeyError:
                    continue
            # Check which is the community with highest density
            new_com = -1
            if len(com_counter.keys()) > 0:
                max_freq = max(com_counter.values())
                best_communities = [com for com, freq in com_counter.items()
                               if (max_freq - freq) < 0.0001]
                # If actual vertex com in best communities, it is preserved
                try:
                    if communities[vertex] in best_communities:
                        new_com = communities[vertex]
                except KeyError:
                    pass
                # If vertex community changes... 
                if new_com == -1:
                    # Set flag of non-convergence
                    cont = True
                    # Randomly chose a new community from candidates
                    new_com = random.choice(best_communities)
                    # Update previous community status
                    try:
                        com_to_numvertices[communities[vertex]] -= 1
                    except KeyError:
                        pass
                    # Update new community status
                    communities[vertex] = new_com
                    com_to_numvertices[communities[vertex]] += 1
        # If maximum iterations reached --> output actual results
        if iter_count > max_iter:
            print 'Exiting by max iterations!'
            break
    # Return results by grouping communities as list of vertices
    return list(_invert_dict(communities).values())

def _invert_dict(orig_dict):
    """
    Inverting Python dictionary keys and values: Many to one --> One to many
    Args:
        - orig_dict: Dictionary desired to invert.
            + type: dict
    Return:
        - Inverted dictionary
            + type: dict
    """
    return_dict = {}
    for v, k in orig_dict.items():
        return_dict[k].add(v)
return return_dict
