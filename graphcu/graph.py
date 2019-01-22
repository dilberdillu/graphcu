#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 19 15:06:21 2018

@author: dillu
"""

from networkx.exception import NetworkXError
import matplotlib.pyplot as plt

class Graph(object):
    
    node_dict_factory = dict
    node_attr_dict_factory = dict
    adjlist_outer_dict_factory = dict
    adjlist_inner_dict_factory = dict
    edge_attr_dict_factory = dict
    graph_attr_dict_factory = dict
    
    
    
    def __init__(self, incoming_graph_data=None, **attr):
        self.graph_attr_dict_factory = self.graph_attr_dict_factory
        self.node_dict_factory = self.node_dict_factory
        self.node_attr_dict_factory = self.node_attr_dict_factory
        self.adjlist_outer_dict_factory = self.adjlist_outer_dict_factory
        self.adjlist_inner_dict_factory = self.adjlist_inner_dict_factory
        self.edge_attr_dict_factory = self.edge_attr_dict_factory
        
        self.graph = self.graph_attr_dict_factory()
        self._node = self.node_dict_factory()
        self._adj = self.adjlist_outer_dict_factory()
        
        '''
        if incoming_graph_data is not None:
            convert.to_networkx_graph(incoming_graph_data, create_using=self)
            
        self.graph.update(attr)
        '''
        
        
    def add_node(self, node_for_adding, **attr):
        #addnode
        if node_for_adding not in self._node:
            self._adj[node_for_adding] = self.adjlist_inner_dict_factory()
            attr_dict = self._node[node_for_adding] = self.node_attr_dict_factory()
            attr_dict.update(attr)
        else:
            self._node[node_for_adding].update(attr)
            
    def update(self, edges=None, nodes=None):
        
        if edges is not None:
            if nodes is not None:
                self.add_nodes_from(nodes)
                self.add_edges_from(edges)
            else:
                try:
                    graph_nodes = edges.nodes
                    graph_edges = edges.edges
                except AttributeError:
                    self.add_edges_from(edges)
                else:
                    self.add_nodes_from(graph_nodes.data())
                    self.add_edges_from(graph_edges.data())
                    self.graph.update(edges.graph)
        elif nodes is not None:
            self.add_nodes_from(nodes)
        else:
            raise NetworkXError("update needs nodes or edges input")
                
        
    def add_nodes_from(self, nodes_for_adding, **attr):
        #add nodes from
        for n in nodes_for_adding:
            try:
                if n not in self._node:
                    self._adj[n] = self.adjlist_inner_dict_factory()
                    attr_dict = self._node[n] = self.node_attr_dict_factory()
                    attr_dict.update(attr)
                else:
                    self._node[n].update(attr)
            except TypeError:
                nn, ndict = n
                if nn not in self._node:
                    self.adj[nn] = self.adjlist_inner_dict_factory()
                    newdict = attr.copy()
                    newdict.update(newdict)
                    attr_dict = self._node[nn] = self.node_attr_dict_factory()
                    attr_dict.update(newdict)
                else:
                    olddict = self._node[nn]
                    olddict.update(attr)
                    olddict.update(ndict)
                
        
        
    def add_edges_from(self, ebunch_to_add, **attr):
       for e in ebunch_to_add:
            ne = len(e)
            if ne == 3:
                u, v, dd = e
            elif ne == 2:
                u, v = e
                dd = {}
            else:
                raise NetworkXError("Egde tuple %s must be a 2-tuple or 3tuple"%(e,))
            if u not in self._node:
                self._adj[u] = self.adjlist_inner_dict_factory()
                self._node[u] = self.node_attr_dict_factory()
            if v not in self._node:
               self._adj[v] = self.adjlist_inner_dict_factory()
               self._node[v] = self.node_attr_dict_factory()
            datadict = self._adj[u].get(v, self.edge_attr_dict_factory())
            datadict.update(attr)
            datadict.update(dd)
            self._adj[u][v] = datadict
            self._adj[v][u] = datadict
            
            

g = Graph()
mylist = tuple([(1,2), (2,6), (2,3), (3,4), (3,5)])
g.add_edges_from(mylist)

h = plt.draw(g)

