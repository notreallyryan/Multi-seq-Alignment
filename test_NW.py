"""
Testing NW file
"""
import pandas as pd
import numpy as np

from NW import NW
from node import node

import unittest
from pandas.testing import assert_frame_equal

#create basic scoring matrix for testing
scores = np.array([[1,-1,-1,-1,-1],[-1,1,-1,-1,-1],[-1,-1,1,-1,-1],[-1,-1,-1,1,-1],[-1,-1,-1,-1,1]])
score_df = pd.DataFrame(scores, index = ['A','C','G','T','-'], columns = ['A','C','G','T','-'])
gap_penalty = [2,2]

scores = np.array([[1,-2,-1,-1,-1],[-2,2,-1,-1,-1],[-1,-1,3,-3,-1],[-1,-1,-3,1,-1],[-1,-1,-1,-1,1]])
score_df2 = pd.DataFrame(scores, index = ['A','C','T','G','-'], columns = ['A','C','T','G','-'])
gap_penalty2 = [3,3]

gap_penalty3 = [3,1]

class MyTest(unittest.TestCase):

    """
    Testing the NW object with gap_add == gap_start
    """

    def test_no_match(self):
        node_1 = node(["A"])
        node_2 = node(["C"])
        testobject = NW(node_1, node_2, score_df, gap_penalty)
        self.assertEqual(-1, testobject.get_score())


    def test_all_match(self):
        node_1 = node(["AA"])
        node_2 = node(["AA"])
        testobject = NW(node_1, node_2, score_df, gap_penalty)
        self.assertEqual(2, testobject.get_score())

    def test_partial_match(self):
        node_1 = node(["AATGAC"])
        node_2 = node(["AACTAC"])
        testobject = NW(node_1, node_2, score_df, gap_penalty)
        self.assertEqual(2, testobject.get_score())
   
    def test_all_blank(self):
        node_1 = node(["AATGAC"])
        node_2 = node(["A"])
        testobject = NW(node_1, node_2, score_df, gap_penalty)
        self.assertEqual(-9, testobject.get_score())

    def test_diff_size(self):
        node_1 = node(["AATGGAC"])
        node_2 = node(["AAC"])
        testobject = NW(node_1, node_2, score_df, gap_penalty)
        self.assertEqual(-5, testobject.get_score())

    def test_blank_optimal(self):
        node_1 = node(["AATGAC"])
        node_2 = node(["AAAC"])
        testobject = NW(node_1, node_2, score_df, gap_penalty)
        self.assertEqual(0, testobject.get_score())
    
    def test_blanks_in_both(self):
        node_1 = node(["TAGCGCGT"])
        node_2 = node(["TACACAGT"])
        testobject = NW(node_1, node_2, score_df, gap_penalty)
        self.assertEqual(1, testobject.get_score())

    """
    Tests with weighted scoring
    """
    
    def test_blank_optimal(self):
        node_1 = node(["ATTG"])
        node_2 = node(["ATCTG"])
        testobject = NW(node_1, node_2, score_df2, gap_penalty2)
        self.assertEqual(5, testobject.get_score())

    def test_mismatch_optimal(self):
        node_1 = node(["ATTTG"])
        node_2 = node(["ATCTG"])
        testobject = NW(node_1, node_2, score_df2, gap_penalty2)
        self.assertEqual(7, testobject.get_score())
    
    """
    test diff gap penalty
    """

    def test_diff_gap_score(self):
        node_1 = node(["ATTTG"])
        node_2 = node(["AG"])
        testobject = NW(node_1, node_2, score_df, gap_penalty3)
        self.assertEqual(-3, testobject.get_score())

    """
    test with profiles
    """

    def test_profiles(self):
        node_1 = node(["ATG", "ACG"])
        node_2 = node(["ACG", "ATT"])
        testobject = NW(node_1, node_2, score_df2, gap_penalty3)
        self.assertEqual(0.75, testobject.get_score())



if __name__ == '__main__':
    unittest.main()

