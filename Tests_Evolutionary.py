# -*- coding: utf-8 -*-

from Evolutionary import Entity
from Evolutionary import Evolutionary
import unittest
import random 

class Test_AE(unittest.TestCase):

    def setUp(self) -> None:
        random.seed(4)
        self.evol1 = Evolutionary(num_indivs = 12, size_indiv = 6, num_iter = 20,alignment="seqs.txt")

    def test1(self):
        with self.assertRaises(TypeError):
            evol2= Evolutionary(num_indivs = "", size_indiv = 6, num_iter = 20,alignment="seqs.txt")
            self.__init__(evol2)

    def test3(self):
        with self.assertRaises(TypeError):
            evol3= Evolutionary(num_indivs = 12, size_indiv = "", num_iter = 20,alignment="seqs.txt")
            self.__init__(evol3)

    def test4(self):
        with self.assertRaises(TypeError):
            evol4= Evolutionary(num_indivs = 12, size_indiv = 6, num_iter = "",alignment="seqs.txt")
            self.__init__(evol4)

    def test5(self):
        with self.assertRaises(TypeError):
            evol5= Evolutionary(num_indivs = 12, size_indiv = 6, num_iter = 20,alignment=30)
            self.__init__(evol5)

    def test6(self):
        self.assertEqual(self.evol1.get_motifs(),['TGACGG', 'TGACCA', 'TGACAG', 'TGACAG', 'TGACAG'])
        

    

if __name__ == "__main__":
    unittest.main()
