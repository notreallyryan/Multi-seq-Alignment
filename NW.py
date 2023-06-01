import numpy as np
import pandas as pd

'''
Object for a Needleman-Wunsch type pairwise alignment
'''
class NW:
    """
    Constructor: Makes the object. Calls the fillgraph function as well.
    Inputs: two node objects (node1 and node2), a scoring pandas dataframe, and a list of the gap penalties.
    """
    def __init__(self, node1, node2, scoring, penalties):
        self.node1 = node1.get_profile()
        self.node2 = node2.get_profile()
        self.scoring = scoring
        self.gapstart = penalties[0]
        self.gapadd = penalties[1]
        
        #creating the NW matrices
        self.fillgraph()
        self.traceback()
    
    """
    Fills out the NW graphs. Accounts for the additional gap peanlty by using two additional graphs. 
    """
    def fillgraph(self):
        #get dimensions for the graphs
        height = len(self.node1.columns)+1
        width =  len(self.node2.columns)+1

        #Initiates the three graphs
        self.top = np.zeros((height, width)) #vertical direction, represents node1
        self.mid = np.zeros((height, width))
        self.low = np.zeros((height, width)) #horizontal direction, represents node2

        #sets the second entry of the first row and column of each graph to 0 - gapstart
        self.top[1][0] = self.mid[1][0] = self.low[1][0] = self.top[0][1] = self.mid[0][1] = self.low[0][1] = -(self.gapstart)

        #calculates the additional gap penalty for the rest of the first row and columns
        for i in range(2, height):
            self.top[i][0] = self.mid[i][0] = self.low[i][0] = self.top[i-1][0] - self.gapadd

        for j in range(2, width):
            self.top[0][j] = self.mid[0][j] = self.low[0][j] = self.top[0][j-1] - self.gapadd

        #calculates the values of the NW graphs
        for i in range(1, height):
            for j in range(1, width):
                self.low[i][j] = max(self.low[i][j-1] - self.gapadd, self.mid[i][j-1] - self.gapstart)
                self.top[i][j] = max(self.top[i-1][j]-self.gapadd, self.mid[i-1][j] - self.gapstart)
                self.mid[i][j] = max(self.low[i][j], self.top[i][j], self.mid[i-1][j-1] + self.position_score(i,j))

    """
    Helper function for fillgraph() that calculates the alignment score for two given indexes on the NW graph 
    """
    def position_score(self, i,j):
        #assumes i is index of character in node1, and j is index for node2
        score = 0

        #gets the probability profile for the given position  
        temp1 = self.node1.loc[:, i-1]
        temp2 = self.node2.loc[:, j-1]

        #calculate the alignment score for that instance
        for x in list(temp1.index):
            for y in list(temp2.index):
                score += (temp1[x] * temp2[y] * self.scoring[x][y])
        return score
    
    """
    Function for tracing backwards through the NW graph. Stores the locations of indexes to put blanks after. 
    For computation sake, the modificatons to the sequences is not done until it has to be. 
    """
    def traceback(self):
        self.blanks1 = [] #list of indexes in node1 after which to insert a blank (vertical)
        self.blanks2 = [] #list of indexes in node2 after which to insert a blank (horizontal)

        #set dimensions 
        i = len(self.node1.columns) #fits index of NW
        j = len(self.node2.columns) #fits index of NW
        seq1_gap = False
        seq2_gap = False

        self.score = 0

        #traverses the NW graph, recording positons after which to put a blank.
        while i >= 1 and j >= 1:
            if self.node1[i-1].equals(self.node2[j-1]):
                self.score += self.position_score(i,j)
                i-=1
                j-=1
                seq1_gap = seq2_gap = False
            elif self.mid[i-1][j-1] >= self.mid[i-1][j] and self.mid[i-1][j-1] >= self.mid[i][j-1]:
                self.score += self.position_score(i,j)
                i-=1
                j-=1
                seq1_gap = seq2_gap = False
            elif self.mid[i-1][j] >= self.mid[i][j-1]:
                self.blanks2.append(j-1)
                i-=1
                if seq2_gap == False: self.score -= self.gapstart
                else: self.score -= self.gapadd
                seq2_gap = True
            else:
                self.blanks1.append(i-1)
                j-=1
                if seq1_gap == False: self.score -= self.gapstart
                else: self.score -= self.gapadd
                seq1_gap = True
        
        #adds in the extra blanks if necessary:
        if i > 0:
            self.score -= ((i-1)* self.gapadd + self.gapstart)
            for x in range(0, i): self.blanks2.append(-1)
        
        if j > 0:
            self.score -= ((j-1)* self.gapadd + self.gapstart)
            for x in range(0, j): self.blanks1.append(-1)
    
    """
    Getter function that returns the maximal score of the alignment (calculated in traceback())
    """
    def get_score(self):
        return self.score
    
    """
    returns both of the blank lists in a list. The first value in the list pertains to the first node, and the second value to the second node
    """
    def get_blanks(self):
        return [self.blanks1, self.blanks2]

