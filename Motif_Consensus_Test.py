# -*- coding: utf-8 -*-
"""
Created on Sun May 15 17:30:41 2022

@author: vania
"""
from Motif_Consensus import Motif_Consensus
from MySeq import MySeq
import unittest
import random


class Test_Motif_Consensus(unittest.TestCase):
    
    def setUp(self) -> None:
        seq1 = MySeq("ATAGAGCATAGA","dna")
        seq2 = MySeq("ACGATAGATGA","dna")
        seq3 = MySeq("AAGATAGGGG","dna")
        seq4 = MySeq("AAGACTTAGGGG","dna")
        
        self.test = Motif_Consensus(4,[seq1,seq2,seq3,seq4])
        self.test2 = Motif_Consensus(2, [seq1])
        self.test3 = Motif_Consensus(5, [seq1, seq4])
        self.test4 = Motif_Consensus()
     
        
    def test_Heuristic(self):
         
         self.assertEqual(self.test.Heuristic(), [0, 3, 3, 5])
         self.assertEqual(self.test2.Heuristic(), [0])
         self.assertEqual(self.test3.Heuristic(), [1, 6])
         self.assertRaises(IndexError, self.test4.Heuristic)
    
    def test_HeuristicStochastic(self):
        random.seed(5)
        self.assertEqual(self.test.HeuristicStochastic(), [2, 5, 5, 7])
        random.seed(5)
        self.assertEqual(self.test2.HeuristicStochastic(), [2])
        random.seed(5)
        self.assertEqual(self.test3.HeuristicStochastic(0.5), [4, 5])
        self.assertRaises(IndexError, self.test4.HeuristicStochastic)
        
    def test_re_motif(self):
        random.seed(5)
        self.assertEqual(self.test.re_motif(self.test.Heuristic()), ['ATAG', 'ATAG', 'ATAG', 'TTAG'] )
        self.assertEqual(self.test2.re_motif(self.test2.Heuristic()), ['AT'] )
        self.assertEqual(self.test3.re_motif(self.test3.HeuristicStochastic()), ['AGCAT', 'TTAGG'] )
        
    def test_score(self):
        self.assertEqual(self.test.score(self.test.Heuristic()), 15)
        random.seed(5)
        self.assertEqual(self.test.score(self.test.HeuristicStochastic(), 0.5), 15.0)
    
    def test_scoreMult(self): 
        self.assertEqual(self.test.scoreMult(self.test.Heuristic()), 0.75)
        random.seed(5)
        self.assertEqual(self.test.scoreMult(self.test.HeuristicStochastic(), 0.5), 0.13671875)
    
        
if __name__ == "__main__":
    unittest.main()