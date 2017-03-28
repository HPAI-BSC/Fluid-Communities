from collections import Counter
import random
from networkx.utils import groups
from networkx.algorithms.community.quality import modularity


def fluid_communities(G, k, max_iter=10):
    """
    Args:
        - G: Networkx Graph object.
            + type: networkx.Graph
        - k: Number of desired communities.
            + type: int
        - max_iter: Maximum number of iterations allowed (default=10).
            + type: int
    Return:
        -  Python list of communities, where each community is a python list containing its belonging vertices.
            + type: list(list(int or string))
    """
    # Initialization
    label_score = 100
    nodes = list(G)
    random.shuffle(nodes)
    labels = {n: i for i, n in enumerate(nodes[:k])}
    score = {}
    label_to_nodes = {}
    for labeled_node in labels.keys():
        label_to_nodes[labels[labeled_node]] = [labeled_node]
        score[labeled_node] = label_score / float(len(label_to_nodes[labels[labeled_node]]))
        
    iter_count = 0 
    cont = True
    while cont:
        # Iteration loop
        cont = False
        iter_count += 1
        nodes = list(G)
        random.shuffle(nodes)
        for node in nodes:
            # Nodes loop
            # Label update rule
            label_scores = Counter()
            # Take into account self label
            try:
                label_scores.update({labels[node]: score[node]})
            except KeyError:
                pass
            # Gather neighbour labels
            for v in G[node]:
                try:
                    label_scores.update({labels[v]: score[v]})
                except KeyError:
                    continue
            # Check which is the label with highest score
            new_label = -1
            if len(label_scores.keys()) > 0:
                max_freq = max(label_scores.values())
                best_labels = [label for label, freq in label_scores.items()
                               if (max_freq - freq) < 0.0001]
                # If actual node label in best labels, it is preserved,
                try:
                    if labels[node] in best_labels:
                        new_label = labels[node]
                except KeyError:
                    pass
                # If label is changed... 
                if new_label == -1:
                    # Set flag of non-convergence
                    cont = True
                    # Randomly chose a new label from candidates
                    new_label = random.choice(best_labels)

                    # Update previous label variables
                    try:
                        label_to_nodes[labels[node]].remove(node)
                        new_score = label_score / float(len(label_to_nodes[labels[node]]))
                        for node_l in label_to_nodes[labels[node]]:
                            score[node_l] = new_score
                    except KeyError:
                        pass

                    # Update new label variables
                    labels[node] = new_label
                    label_to_nodes[labels[node]].append(node)
                    new_score = label_score / float(len(label_to_nodes[labels[node]]))
                    for node_l in label_to_nodes[labels[node]]:
                        score[node_l] = new_score

        # If maximum iterations reached --> output actual results
        if iter_count > max_iter:
            #print 'Exiting by max iterations!'
            break
    return list(groups(labels).values())

