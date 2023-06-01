"""
Testing node file
"""
import pandas as pd
import numpy as np

from node import node
import unittest
from pandas.testing import assert_frame_equal


class MyTest(unittest.TestCase):

    """
    Testing the node object
    """
    
    #test the profile calculations
    def test_profile_calc_all_split(self):
        test = node(["ACGT-", "-TCGA"])
        calculated = np.array([[0.5,0,0,0,0.5],[0,0.5,0.5,0,0],[0,0,0.5,0.5,0],[0,0.5,0,0.5,0],[0.5,0,0,0,0.5]])
        correct = pd.DataFrame(calculated, index = ['A','C','G','T','-'])
        assert_frame_equal(test.get_profile(), correct)

    def test_profile_calc_all_match(self):
        test = node(["AAAAA", "AAAAA"])
        calculated = np.array([[1.0,1.0,1.0,1.0,1.0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]])
        correct = pd.DataFrame(calculated, index = ['A','C','G','T','-'])
        assert_frame_equal(test.get_profile(), correct)
    
    def test_profile_calc_some_match(self):
        test = node(["AGAAA", "AA-AA"])
        calculated = np.array([[1.0,0.5,0.5,1.0,1.0],[0,0,0,0,0],[0,0.5,0,0,0],[0,0,0,0,0],[0,0,0.5,0,0]])
        correct = pd.DataFrame(calculated, index = ['A','C','G','T','-'])
        assert_frame_equal(test.get_profile(), correct)

    #tests the update function
    def test_add_blank_start(self):
        test = node(["ACGT-"])
        self.assertEqual(test.get_update([-1]),["-ACGT-"])
    
    def test_add_blank_end(self):
        test = node(["ACGT-"])
        self.assertEqual(test.get_update([4]),["ACGT--"])
    
    def test_add_blanks_alternating(self):
        test = node(["ACGT-"])
        self.assertEqual(test.get_update([4,3,2,1,0,-1]),["-A-C-G-T---"])
    
    def test_add_blanks_multiseq(self):
        test = node(["ACGT-", "TCG-A"])
        self.assertEqual(test.get_update([4,3,2,1,0,-1]),["-A-C-G-T---", "-T-C-G---A-"])

    def test_rightblanked(self):
        test = node(["ACGT-"])
        self.assertEqual(test.get_update([4,4,4,4]),["ACGT-----"])
   
    def test_leftblanked(self):
        test = node(["ACGT-"])
        self.assertEqual(test.get_update([-1,-1,-1,-1]),["----ACGT-"])


if __name__ == '__main__':
    unittest.main()

