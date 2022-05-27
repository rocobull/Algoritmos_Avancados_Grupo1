# -*- coding: utf-8 -*-

from GibbsSampling import GibbsSampling
import random
import unittest


class TestGibbsSampling1(unittest.TestCase):

	def setUp(self):
		random.seed(3)
		self.gs = GibbsSampling(["GTAAACAATATTTATAGC", "AAAATTTATATCGCAAGG", "CCTTTATACTCAAGCGTG", "TGATTTATAGACGTCCCA"], "ATCG", 6)

	def test_get_motifs1(self):
		self.assertEqual(self.gs.get_motifs(6), ['TTTATA', 'TTTATA', 'TTTATA', 'TTTATA'])


class TestGibbsSampling2(unittest.TestCase):

	def setUp(self):
		random.seed(3)
		self.gs = GibbsSampling(["thequickdog", "browndoggie", "doggoeswild"], "ABCDEFGHIJKLMNOPQRSTUVWXYZ", 3)

	def test_get_motifs1(self):
		self.assertEqual(self.gs.get_motifs(3), ['DOG', 'DOG', 'DOG'])


class RaisesGibbsSampling(unittest.TestCase):

	######## assertRaises na criação de uma instância ########

	def test_is_list(self):
		with self.assertRaises(TypeError):
			gs = GibbsSampling("GTAAACAATATTTA AAAATTTATATCGC CCTTTATACTCAAG TGATTTATAGACGT", "ATCG", 4)

	def test_is_str(self):
		with self.assertRaises(TypeError):
			gs = GibbsSampling(["GTAAACAATATTTA", ["AAAATTTATATCGC"], "CCTTTATACTCAAG", "TGATTTATAGACGT"], "ATCG", 4)

	def test_is_str2(self):
		with self.assertRaises(TypeError):
			gs = GibbsSampling(["GTAAACAATATTTA", "AAAATTTATATCGC", "CCTTTATACTCAAG", "TGATTTATAGACGT"], ["ATCG"], 4)

	def test_is_int(self):
		with self.assertRaises(TypeError):
			gs = GibbsSampling(["GTAAACAATATTTA", "AAAATTTATATCGC", "CCTTTATACTCAAG", "TGATTTATAGACGT"], "ATCG", "4")

	def test_in_interval1(self):
		with self.assertRaises(ValueError):
			gs = GibbsSampling(["GTAAACAATATTTA", "AAAATTTATATCGC", "CCTTTATACTCAAG", "TGATTTATAGACGT"], "ATCG", 1)

	def test_in_interval2(self):
		with self.assertRaises(ValueError):
			gs = GibbsSampling(["GTAAACAATATTTA", "AAAATTTATATCGC", "CCTTTATACTCAAG", "TGATTTATAGACGT"], "ATCG", 20)

	######## assertRaises na chamada do método search_pattern() ########

	def setUp(self):
		self.gs = GibbsSampling(["GTAAACAATATTTA", "AAAATTTATATCGC", "CCTTTATACTCAAG", "TGATTTATAGACGT"], "ATCG", 4)

	def test_is_str3(self):
		with self.assertRaises(TypeError):
			self.gs.get_motifs("4")

	def test_in_interval3(self):
		with self.assertRaises(ValueError):
			self.gs.get_motifs(0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
