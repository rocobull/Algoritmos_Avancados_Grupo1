# -*- coding: utf-8 -*-

from BurrowsWheeler import BurrowsWheeler
import unittest


class TestBurrowsWheeler1(unittest.TestCase):

	def setUp(self):
		self.bw = BurrowsWheeler("ATCGGTAGTTTCGATTTA")

	def test_compress(self):
		self.assertEqual(self.bw.compress(), "ATT$GTTCCGATGTATTAG")

	def test_search_pattern(self):
		self.assertEqual(self.bw.search_pattern("TCG"), [1, 10])


class TestBurrowsWheeler2(unittest.TestCase):

	def setUp(self):
		self.bw = BurrowsWheeler("AGAGAGAGAGAGAAA")

	def test_compress(self):
		self.assertEqual(self.bw.compress(), "3A6G1$6A")

	def test_search_pattern(self):
		self.assertEqual(self.bw.search_pattern("AG"), [0, 2, 4, 6, 8, 10])


class RaisesBurrowsWheeler(unittest.TestCase):

	######## assertRaises na criação de uma instância ########

	def test_is_str(self):
		with self.assertRaises(TypeError):
			bw = BurrowsWheeler(["ATCGGTAGTTTCGATTTA"])

	######## assertRaises na chamada do método search_pattern() ########

	def setUp(self):
		self.bw = BurrowsWheeler("AGAGAGAGAGAGAAA")

	def test_is_str2(self):
		with self.assertRaises(TypeError):
			self.bw.search_pattern(["TCG"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
