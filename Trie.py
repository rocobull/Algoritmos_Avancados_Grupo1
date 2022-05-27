# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 00:12:37 2022

@author: rober
"""

import pprint

class Trie:
    """
    Contrói uma árvore trie de acordo com os padrões inseridos para a procura
    de padrões em sequências
    """
    
    def __init__(self, seqs:list = None):
        """
        Guarda a árvore trie e os padrões inseridos na árvore
        
        Parameters
        ----------
        :param seqs: Uma lista de padrões a serem inseridas na árvore
        """
        self.seqs = []
        self.dic = {}
        if seqs != None:
            self.seqs = seqs
            for seq in seqs:
                self.insert_pat(seq)
        
    
    def __str__(self):
        """
        Imprime a árvore trie num formato legível
        """
        return pprint.pformat(self.dic, indent=1)
    
        
    def get_seqs(self) -> list:
        """
        Devolve a lista de sequências usadas na árvore trie
        """
        return self.seqs
        
        
    def insert_pat(self, pattern:str):
        """
        Insere um ou mais padrões à árvore trie
        
        Parameters
        ----------
        :param pattern: Um padrão ou lista de padrões a serem inseridos na árvore trie
        """
        if type(pattern) == str:
            pattern = [pattern]
            
        for pat in pattern:
            dic = self.dic
            for p in pat:
                if p not in dic:
                    dic[p] = {}
                dic = dic[p]
            dic["$" + pat] = 0
        
            if pat not in self.seqs:
                self.seqs.append(pat)
            
    
    def check_pat(self, pat:str) -> bool:
        """
        Verifica se a sequência pertence à árvore trie (True) ou não (False)
        
        Parameters
        ----------
        :param pat: Um padrão a ser procurado na árvore trie
        """
        dic = self.dic
        for p in pat:
            if p not in dic:
                return False
            dic = dic[p]
        if "$"+pat in dic:
            return True
        else:
            return False
        
    
    def prefix_trie_match(self, text:str) -> list:
        """
        Devolve uma lista de prefixos da sequência especificada que pertencem
        à árvore trie
        
        Parameters
        ----------
        :param text: Sequência a ser processada por suffixos pertencentes à árvore trie
        """
        all_prefix = [text[0:ix] for ix in range(len(text)+1)]
        result = []
        for al in all_prefix:
            if self.check_pat(al):
                result.append(al)
        return result
        
    
    def trie_matches(self, text:str) -> list:
        """
        Devolve uma lista de tuplos incluindo as sub-sequências da sequência especificada
        que pertencem à árvore trie e os seus respetivos índices na sequência
        
        Parameters
        ----------
        :param text: Sequência a ser processada por sub-sequências pertencentes à árvore trie
        """
        suffixes = [text[ix:] for ix in range(len(text))]
        result = []
        for ix,suf in enumerate(suffixes):
            for res in self.prefix_trie_match(suf):
                result.append((res, ix))
        return result
