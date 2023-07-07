from os.path import dirname, abspath
from os import listdir
from os.path import isfile, join
import re
from numpy import genfromtxt
from pandas import DataFrame
import csv

class Reader:

    def __init__(self) -> None:
        pass



    def get_seqs(self):
        d = dirname(abspath(__file__)) + "/_INPUTS/sequences"
        if len(listdir(d)) == 0: return []
        
        self.seq_files = [f for f in listdir(d) if isfile(join(d, f))]
        if '.DS_Store' in self.seq_files: self.seq_files.remove('.DS_Store')

        sequences = []
        id = -1

        for seq_file in self.seq_files:
            f = open(d + "/" + seq_file, 'r')
            lines = f.readlines()
            hre = re.compile('>(\S+)')
            lre = re.compile('^(\S+)$')
            
            for line in lines:
                outh = hre.search(line)
                if outh: 
                    id += 1
                else:
                    outl = lre.search(line)
                    if outl == None: continue #deletes any nasty blanks >:(
                    elif len(sequences) != id: sequences[id] += outl.group(1)
                    else: sequences.append(outl.group(1))

        return sequences
    


    def get_scoring(self):
        d = dirname(abspath(__file__)) + "/_INPUTS/scoring"
        if len(listdir(d)) == 0: return None
        
        if listdir(d)[0] != ".DS_Store":
            self.scoring_file = d + "/" + listdir(d)[0]
        else: self.scoring_file = d + "/" + listdir(d)[1]
        
        matrix = genfromtxt(self.scoring_file, delimiter=',')
        
        matrix = matrix[0:4, 0:4] #only select first 4 by 4
        score_df = DataFrame(matrix, index = ['A','C','G','T'], columns = ['A','C','G','T']) #convert to pandas dataframe
        return score_df