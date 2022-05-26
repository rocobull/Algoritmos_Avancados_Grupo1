# -*- coding: utf-8 -*-
"""
Created on Sun May 15 19:04:51 2022

@author: rober
"""

from Automato import Automato
import unittest

class TestAutomato(unittest.TestCase):
    
    def test_procura(self):
        alpha = "aBcD"
        pat1 = "bdCA"
        pat2 = ""
        text1 = "bdcaabcdbacabdcadbcabcbacabdcabaabdca"
        text2 = "aaaaaaaaaaaaaaa"
        
        test = Automato(alpha,pat1)
        self.assertEqual(test.af(text1), [0,12,26,33])
        self.assertEqual(test.af(text2), [])
        
        test = Automato(alpha,pat2)
        self.assertEqual(test.af(text1), [])
        self.assertEqual(test.af(text2), [])
        
        self.assertRaises(AssertionError, test.af,"abcde")
        self.assertRaises(AssertionError, Automato, alpha, "abcde")
    


if __name__ == "__main__":
    unittest.main()