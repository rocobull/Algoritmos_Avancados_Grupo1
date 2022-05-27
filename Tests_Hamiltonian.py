# -*- coding: utf-8 -*-

from Hamiltonian import Hamiltonian
import unittest


class TestsHamiltonian(unittest.TestCase):

	def setUp(self):
		kmers1 = ['ATG','TGC','GCG','CGT','GTA','TAG','AGT','GTG','TGC','GCA','CAG','AGT','GTG','TGT','GTA','TAC','ACA','CAC']
		self.dbr1 = Hamiltonian(kmers1)
		kmers2 = ['ATG','TGC','GCG','CGT','GTA','TAG','AGT','GTG','TGC','GCA','CAG','AGT','GTG','TGT','GTA','TAC','ACA','CAC','ACT']
		self.dbr2 = Hamiltonian(kmers2)

	def test_rebuild_seq1(self):
		self.assertEqual(self.dbr1.rebuild_seq(), 'ATGCACAGTAGTGCGTGTAC')

	def test_rebuild_seq2(self):
		self.assertEqual(self.dbr2.rebuild_seq(), 'ATGCACAGTAGTGCGTGTACT')


class RaisesHamiltonian(unittest.TestCase):

	def setUp(self):
		self.input1 = 'ATGCGTAGTGTGCACAGTAC'
		self.input2 = ['ATG',['TGC'],'GCG','CGT','GTA','TAG','AGT','GTG','TGC','GCA','CAG','AGT','GTG','TGT','GTA','TAC','ACA','CAC']

	def test_is_list(self):
		with self.assertRaises(TypeError):
			dbr = Hamiltonian(self.input1)

	def test_is_str(self):
		with self.assertRaises(TypeError):
			dbr = Hamiltonian(self.input2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
