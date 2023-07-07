from os.path import dirname, abspath
from os import listdir
from os.path import isfile, join
import re
from numpy import genfromtxt
from pandas import DataFrame
import csv

class Reader:

    def __init__(self) -> None:
        d = dirname(dirname(abspath(__file__))) + "/_INPUTS/sequences"
        self.seq_files = [f for f in listdir(d) if isfile(join(d, f))]
        if '.DS_Store' in self.seqs: self.seqs.remove('.DS_Store')

        d = dirname(dirname(abspath(__file__))) + "/_INPUTS/scoring"
        self.scoring_file = listdir(d)[0]




    def get_seqs(self):

        sequences = []
        for seq_file in self.seq_files:
            f = open(seq_file, 'r')
            lines = f.readlines()
            hre = re.compile('>(\S+)')
            lre = re.compile('^(\S+)$')
            
            id = -1
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
        matrix = genfromtxt(self.scoring_file, delimiter=',')
        matrix = matrix[0:4, 0:4] #only select first 4 by 4
        score_df = DataFrame(matrix, index = ['A','C','G','T'], columns = ['A','C','G','T']) #convert to pandas dataframe
        return score_df