# -*- coding: utf-8 -*-

"""
Class: MySeq
"""

class MySeq:

    def __init__(self, seq:str , tipo:str ="dna"):
        """
        Recebe 1 sequência de DNA, RNA ou AA e o seu tipo

        Parameters
        ----------
        :param seq: sequência 
        :param tipo:alfabeto da sequência - dna,rna ou aa.

        """
        self.seq = seq.upper()
        self.tipo = tipo

    def __len__(self):
        """
        Devolve cumprimento da sequência
        """
        return len(self.seq)
    
    def __getitem__(self, n:int)->str:
        """
        Devolve elemento do indice fornecido
        
        Parameters
        ----------
        :param n: indice
        """
        return self.seq[n]

    def __getslice__(self, i:int, j:int)->str:
        """
        Devolve sequência entre dois indices fornecidos
        
        Parameters
        ----------
        :param i: indice inicial
        :param j: indice final
        """
        return self.seq[i:j]

    def __str__(self)->str:
        """
        Devolve o tipo e a seqência guardada
        """        
        return self.tipo + ":" + self.seq

    def printseq(self):
        """
        Devolve a seqência guardada
        """   
        print(self.seq)
    
    def alfabeto(self):
        """
        Devolve o tipo da sequência guardada
        """  
        if (self.tipo=="dna"): return "ACGT"
        elif (self.tipo=="rna"): return "ACGU"
        elif (self.tipo=="protein"): return "ACDEFGHIKLMNPQRSTVWY"
        else: return None
    
