# -*- coding: utf-8 -*-

from BoyerMoore import BoyerMoore
import unittest

class TestBoyerMoore(unittest.TestCase):
    
    def test_procura(self):
        alpha = "1234"
        pat = "333"
        text = "444444333333222222111111"
        
        test = BoyerMoore(alpha,pat)
        self.assertEqual(test.procura(text,False), [6,9])
        self.assertEqual(test.procura(text,True), [6,7,8,9])
        self.assertEqual(test.procura("111111"), [])
        self.assertRaises(AssertionError, test.procura,"outra_coisa",True)
        
        alpha = "abc"
        pat1 = ""
        pat2 = "abcd"
        self.assertRaises(AssertionError, BoyerMoore, alpha, pat1)
        self.assertRaises(AssertionError, BoyerMoore, alpha, pat2)
    


if __name__ == "__main__":
    unittest.main()
