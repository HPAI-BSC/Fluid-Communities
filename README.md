# Fluid-Communities

Fluid Communities (FluidC) is a novel community detection algorithm based on the simple idea of fluids interacting in an environment, expanding and contracting. It is propagation-based algorithm but, up to our knowledge, it is the first of its kind that allow to specify the number of desired communities (k). Check out our paper "Fluid Communities: A Community Detection Algorithm" [https://arxiv.org/abs/1703.09307] for more details.

Right now, FluidC is implemented in Python and it works with Networkx graph objects [https://github.com/networkx/networkx]. However, we are planning on developing an additional implementation in C++ to allow the usage of FluidC under the python-igraph library.
