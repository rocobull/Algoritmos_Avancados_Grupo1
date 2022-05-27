# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 00:12:37 2022

@author: rober
"""

"""
Class: Trie
"""


import pprint
import re
from typing import Union

class Trie:
    """
    Contrói uma árvore trie de acordo com os padrões inseridos para a procura
    de padrões em sequências
    """
    
    def __init__(self, pats: Union[str,list,tuple,None] = None):
        """
        Guarda a árvore trie e os padrões inseridos na árvore
        
        Parameters
        ----------
        :param seqs: Uma lista de padrões a serem inseridas na árvore
        """
        self.pats = []
        self.dic = {}
        
        if pats != None:
            self.add_pats(pats)
        
    
    def __str__(self):
        """
        Imprime a árvore trie num formato legível
        """
        return pprint.pformat(self.dic, indent=1)
    
        
    def get_pats(self) -> list:
        """
        Devolve a lista de padrões usadas na árvore trie
        """
        return self.pats
        
    
    def add_pats(self, pattern: Union[str,list,tuple]):
        """
        Adiciona um ou mais padrões à lista de sequências e à árvore trie
        
        Parameters
        ----------
        :param pattern: Padrão/padrões a serem inseridos na lista de padrões e na árvore trie
        """
        if type(pattern)==str:
            self._insert_pat(pattern)
        else:
            for pat in pattern:
                self._insert_pat(str(pat))
        
    
    def _insert_pat(self, pattern:str):
        """
        Insere um padrão à árvore trie
        
        Parameters
        ----------
        :param pattern: Padrão a ser inserido na árvore trie
        """
        assert type(pattern)==str, "Atributo 'pattern' deve ser do tipo 'str'"
        
        pattern = pattern.upper()
        if pattern not in self.pats:
            self.pats.append(pattern)
            dic = self.dic
            for p in pattern:
                if p not in dic:
                    dic[p] = {}
                dic = dic[p]
            dic["$" + pattern] = 0
        
        
    def rm_pats(self, pattern: Union[str,list,tuple]):
        """
        Remove um padrão (ou vários padrões) da lista de sequências e da árvore trie
        
        Parameters
        ----------
        :param pattern: Padrão/Lista de padrões a serem removidos da lista de padrões e da árvore trie
        """
        assert hasattr(pattern, "__iter__") or type(pattern)==str, "Atributo 'pattern' deve ser um vetor ou do tipo 'str'"
        
        if type(pattern)==str:
            self._rm_pats(pattern)
        else:
            for pat in pattern:
                self._rm_pats(str(pat))
        
        
    def _rm_pats(self, pattern:str):
        """
        Remove um padrão da lista de sequências e da árvore trie
        
        Parameters
        ----------
        :param pattern: Padrão a ser removido da lista de padrões e da árvore trie
        """
        assert type(pattern)==str, "Atributo 'pattern' deve ser do tipo 'str'"
        
        pattern = pattern.upper()
        if pattern not in self.pats:
            print("O padrão não foi inserida na lista de padrões")
            return False
        else:
            self.pats.remove(pattern) #Remover padrão da lista de padrões
            dic = self.dic
            for p in pattern:
                dic = dic[p]
            del dic["$"+pattern] #Remover padrão da árvore trie
            
            #Eliminar caminhos vazios
            for i in range(len(pattern)-1):
                dic = self.dic
                for elem in range(len(pattern)-1-i):
                    dic = dic[pattern[elem]]
                if len(dic[pattern[elem+1]].keys()) == 0:
                    del dic[pattern[elem+1]]
                else:
                    break
            
            #Remover primeiro elemento caso tenha como valor um dicionário vazio
            if len(self.dic[pattern[0]].keys()) == 0:
                del self.dic[pattern[0]]
            return True
        
    
    def check_pat(self, pat:str) -> bool:
        """
        Verifica se o padrão pertence à árvore trie (True) ou não (False)
        
        Parameters
        ----------
        :param pat: Um padrão a ser procurado na árvore trie
        """
        pat = pat.upper()
        dic = self.dic
        for p in pat:
            if p not in dic:
                return False
            dic = dic[p]
        if "$"+pat in dic:
            return True
        else:
            return False
    
    
    def trie_matches(self, text:str) -> list:
        """
        Devolve uma lista de tuplos incluindo as sub-sequências da sequência especificada
        que pertencem à árvore trie e os seus respetivos índices na sequência
        
        Parameters
        ----------
        :param text: Sequência a ser processada por sub-sequências pertencentes à árvore trie
        """
        assert type(text)==str, "Parâmetro 'text' deve ser do tipo 'str'"
        
        text = text.upper()
        result = []
        
        #Analizar os tamanhos dos padrões para procurá-los no texto (diminui o tempo de procura)
        lengths = set([len(pat) for pat in self.pats])
        for l in lengths:
            dots = "."*l
            frags = re.findall(rf"(?=({dots}))", text)
            for ix,frag in enumerate(frags):
                if self.check_pat(frag):
                    result.append((frag,ix))
        return result
        
    

if __name__ == "__main__":
    x = Trie()
    x.add_pats(["ACGT","AAAAAT", "T", "CGAT", "TA"])
    #print()
    #print(x.trie_matches("CGATTACTATCGACGACATCATGC"))
    #print()
    #print(x)
    x.rm_pats("X")
    x.rm_pats(["xxxx", "CGAT"])
    x.dic
    #print(x)
    print(x.trie_matches("ATCGAGCAAAAATAGCGAT"))