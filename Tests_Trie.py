# -*- coding: utf-8 -*-

from Trie import Trie
import numpy as np
import unittest

class Tests_Trie(unittest.TestCase):
    
    def test_trie(self):
        test = Trie()
        
        list_pats = ["aaa","aba",1,"bbb","bab"]
        test.add_pats(list_pats)
        self.assertEqual(test.get_pats(), [str(l).upper() for l in list_pats])
        self.assertEqual(test.dic, {"A":{"A":{"A":{"$AAA":0}}, "B":{"A":{"$ABA":0}}}, "1":{"$1":0},
                                    "B":{"B":{"B":{"$BBB":0}}, "A":{"B":{"$BAB":0}}}})
        
        test.rm_pats("bbb")
        test.rm_pats(np.array(["xxxx","yyyy","aba","zzzz"]))
        self.assertEqual(test.dic, {"A":{"A":{"A":{"$AAA":0}}}, "1":{"$1":0},
                                    "B":{"A":{"B":{"$BAB":0}}}})
        
        text1 = "xxxxxxxxx"
        text2 = 1234
        text3 = "AaAaBbBbAb 1zzzz1 "
        self.assertEqual(test.trie_matches(text1), [])
        self.assertRaises(AssertionError, test.trie_matches, text2)
        self.assertEqual(test.trie_matches(text3), [("1",11),("1",16),("AAA",0),("AAA",1),("BAB",7)])
        
        


if __name__ == "__main__":
    unittest.main()
