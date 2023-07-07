"""
Testing node file
"""
import pandas as pd
import numpy as np
import sys
sys.path.insert(0,".")

from Aligner import Aligner
import unittest
from pandas.testing import assert_frame_equal

scores = np.array([[1,-1,-1,-1],[-1,1,-1,-1],[-1,-1,1,-1],[-1,-1,-1,1]])
score_df = pd.DataFrame(scores, index = ['A','C','G','T'], columns = ['A','C','G','T'])
gap_penalty = [2,2]

scores = np.array([[1,-2,-1,-1],[-2,2,-1,-1],[-1,-1,3,-3],[-1,-1,-3,1]])
score_df2 = pd.DataFrame(scores, index = ['A','C','T','G'], columns = ['A','C','T','G'])
gap_penalty2 = [3,3]

gap_penalty3 = [3,1]

class MyTest(unittest.TestCase):



    """
    Testing the aligner object object with just two sequences.
    """
    def test_complete_match(self):
        testobject = Aligner(["ACG", "ACG"], score_df, gap_penalty)
        self.assertEqual(testobject.Align_sequences(), ["ACG", "ACG"])
    
    def test_spaces(self):
        testobject = Aligner(["TTG", "TAGGG"], score_df2, gap_penalty)
        self.assertEqual(sorted(testobject.Align_sequences()), sorted(["TT--G", "TAGGG"]))
    


    """
    Testing the aligner object object with more sequences.
    """
    def test_three_similar(self):
        testobject = Aligner(["TTG", "TAGGG", "TG"], score_df2, gap_penalty)
        print(testobject.Align_sequences())
    
    def test_two_similar_one_diff(self):
        testobject = Aligner(["TTG", "TAGGG", "CAAT"], score_df2, gap_penalty3)
        print(testobject.Align_sequences())
    
    def test_four_similar(self):
        testobject = Aligner(["ATCTCTATTGGGGATCGGTGGTAGCTAGGAT", "ATCTCTATTCGGGATCGATGGTAGCTAGGAT", "ATCTCTACTCGGGATCGATGGTAGCTACGAT", "ATCTCCACTCGGGATCGATGGTAGCTACGAT"], score_df2, gap_penalty3)
        print(testobject.Align_sequences())

    def test_four_spaced(self):
        testobject = Aligner(["CATGCGAGTAGTAG", "CATGGTAGTAG", "CCTGGAGTACGTAG", "CATGAGCGTAG"], score_df2, gap_penalty3)
        print(testobject.Align_sequences())

       
        
if __name__ == '__main__':
    unittest.main()
