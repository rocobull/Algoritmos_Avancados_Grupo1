# -*- coding: utf-8 -*-

from DeBruijn import DeBruijn
import unittest


class TestsDeBruijn(unittest.TestCase):

	def setUp(self):
		kmers1 = ['ATG','TGC','GCG','CGT','GTA','TAG','AGT','GTG','TGC','GCA','CAG','AGT','GTG','TGT','GTA','TAC','ACA','CAC']
		self.dbr1 = DeBruijn(kmers1)
		kmers2 = ['ATG','TGC','GCG','CGT','GTA','TAG','AGT','GTG','TGC','GCA','CAG','AGT','GTG','TGT','GTA','TAC','ACA','CAC','ACT']
		self.dbr2 = DeBruijn(kmers2)
		kmers3 = ['ATG','TGC','GCG','CGT','GTA','TAG','AGT','GTG','TGC','GCA','CAG','AGT','GTG','TGT','GTA','TAC','ACA','CAT']
		self.dbr3 = DeBruijn(kmers3)

	def test_rebuild_seqs1(self):
		self.assertEqual(self.dbr1.rebuild_seqs(), ['ATGCGTAGTGTGCACAGTAC'])

	def test_rebuild_seqs2(self):
		self.assertEqual(self.dbr2.rebuild_seqs(), ['ATGCGTAGTGTGCACAGTACT'])

	def test_rebuild_seqs3(self):
		self.assertEqual(self.dbr3.rebuild_seqs(), ['ACATGCGTAGTGTGCAGTAC'])


class RaisesDeBruijn(unittest.TestCase):

	def setUp(self):
		self.input1 = 'ATGCGTAGTGTGCACAGTAC'
		self.input2 = ['ATG',['TGC'],'GCG','CGT','GTA','TAG','AGT','GTG','TGC','GCA','CAG','AGT','GTG','TGT','GTA','TAC','ACA','CAC']

	def test_is_list(self):
		with self.assertRaises(TypeError):
			dbr = DeBruijn(self.input1)

	def test_is_str(self):
		with self.assertRaises(TypeError):
			dbr = DeBruijn(self.input2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
