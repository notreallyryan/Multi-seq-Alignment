import pandas as pd
import numpy as np
from node import node
from NW import NW

"""
Produces the best sequence alignment using verified information
"""
class Aligner:
    """
    Constructor: Creates a graph represented by a list of nodes and ajacency matrix of edges
    Inputs: list of sequences to align, scoring matrix (dataframe), penalty list
    """
    def __init__(self, sequences, scorings, penalties):
        #makes a list of all the nodes made from the sequences.
        self.nodes = []
        for string in sequences:
            self.nodes.append(node([string]))
        self.matrix = [] #initiates the edge matrix
        
        #update the scoring dataframe with the "-" option
        self.scorings = scorings
        self.scorings.loc["-"] = -1
        self.scorings.loc[:,["-"]] = -1
        self.scorings.at["-", '-'] = 1

        self.penalties = penalties

    """
    makes the ajacency matrix from the list of given nodes. 
    Each edges contains a NW object or NW child.
    """
    def make_graph(self):
        for i in range(0, len(self.nodes)):
            temp = []
            for j in range(0,i):
                temp.append(NW(self.nodes[i], self.nodes[j],self.scorings, self.penalties))
            self.matrix.append(temp)
    
    """
    removes a node from the graph and from the list
    inputs: index of node in list
    """
    def remove_node(self, index):
        for i in range(index+1, len(self.nodes)):
            del self.matrix[i][index]
        del self.matrix[index]
        del self.nodes[index]

    """
    modifies a node in the graph and recalculates all it's edges
    Inputs: index of node in list
    """
    def modify_node(self, index, newnode):
        for i in range(index+1,len(self.nodes)):
            self.matrix[i][index] = NW(self.nodes[i], newnode, self.scorings, self.penalties)
            pass
        
        for j in range(1,len(self.matrix[index])):
            self.matrix[index][j] = NW(newnode, self.nodes[j], self.scorings, self.penalties)
            pass

        self.nodes[index]= newnode

    """
    Aligns the sequences currently in the object.
    Returns a list of the aligned sequences. 
    """
    def Align_sequences(self):
        #start by making the graph
        self.make_graph()

        #repeat until there is only one node left
        while len(self.nodes) > 1:
            best_larger_index = 0
            best_smaller_index = 0
            best_score = float('-inf')

            #finds global alignment combination with best score
            for i in range(0, len(self.matrix)):
                for j in range(0, len(self.matrix[i])):
                    current_score = self.matrix[i][j].get_score()
                    if  current_score > best_score:
                        best_score = current_score
                        best_larger_index = i
                        best_smaller_index = j

            #gets blanks from the best NW object and uses it to get updated sequences from node objects
            blanks = self.matrix[best_larger_index][best_smaller_index].get_blanks()
            newseq1 = self.nodes[best_larger_index].get_update(blanks[0])
            newseq2 = self.nodes[best_smaller_index].get_update(blanks[1])
            newnode = node(newseq1 + newseq2)

            #updates graph and list
            self.remove_node(best_larger_index)
            self.modify_node(best_smaller_index,newnode)
            
        #return sequences stored in final node
        return self.nodes[0].get_sequences()
