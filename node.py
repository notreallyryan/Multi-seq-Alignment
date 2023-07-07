import pandas as pd
import numpy as np
"""
Code representation of a node in the alignment graph.
"""

class node:

    def __init__(self, data):
        self.data = data #list of the seqeunces in this node
        self.size = len(data)
        self.calculate_profile()



    """
    Calculates the profile for the Node
    """
    def calculate_profile(self):
        #creates an empty dataframe with row names ACGT-
        self.profile = pd.DataFrame(index = ['A','C','G','T','-'])

        #calculate probability of each position and adds to the dataframe as a column. 
        for position in range(0,len(self.data[0])):
            self.profile[position] = 0
            for sequence in self.data:
                self.profile.at[sequence[position], position] += 1/self.size



    """
    returns the profile of the Node 
    """
    def get_profile(self):
        return self.profile
    


    """
    returns the sequences of the Node
    """
    def get_sequences(self):
        return self.data
    

    
    """
    returns an updated list of the sequences in this node with blanks inserted after the indexes recorded in the blanks list.
    Assumes blanks is in decreasing order.
    """
    def get_update(self, blanks):
        #makes copy of the data in the node
        modlist = self.data.copy()

        #modifies the data.
        for i in blanks:
            #does so for each sequence in the data list
            for j in range(0, self.size):
                modlist[j] = modlist[j][:i+1] + "-" + modlist[j][i+1:]

        return modlist

