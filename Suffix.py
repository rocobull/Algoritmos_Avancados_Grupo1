# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 00:13:03 2022

@author: rober
"""

import pprint

class SuffixTree:
    """
    Cria uma árvore de suffixos de um padrão especificado para serem procurados
    em sequências
    """
    
    def __init__(self, pattern:str = ""):
        """
        Cria a árvore de suffixos de acordo com o padrão especificado
        
        Parameters
        ----------
        :param pattern: Padrão usado para criar a árvore de sufixos
        """
        self.dic = {}
        self.set_pat(pattern)
        
        
    def __str__(self) -> str:
        """
        Imprime a árvore de sufixos de forma legível
        """
        return pprint.pformat(self.dic, indent=1)
        
        
    def get_pat(self) -> str:
        """
        Devolve o padrão usado para criar a árvore de sufixos
        """
        return self.pat
    
    
    def set_pat(self, pat:str):
        """
        Define/redefine o padrão para criar/recriar a árvore de sufixos
        
        Parameters
        ----------
        :param pat: Um padrão a partir do qual é criado a árvore de sufixos
        """
        self.pat = pat
        self.sub_pat = [pat[ix:] for ix in range(len(pat))]
        
        for sub in self.sub_pat:
            self.suffix(sub)
        
        
    def suffix(self, pat:str):
        """
        Cria a árvore de sufixos a partir do padrão especificado
        
        Parameters
        ----------
        :param pat: Um padrão a partir do qual é criado a árvore de sufixos
        """
        dic = self.dic
        for p in pat:
            if p not in dic:
                dic[p] = {}
            dic = dic[p]
        dic["$"] = len(self.pat) - len(pat)
        
        
    def get_leafs_below(self, dic:dict) -> list:
        """
        Devolve uma lista de todos os índices abaixo do nodo especificado da árvore
        
        Parameters
        ----------
        :param dic: Uma nodo da árvore (parte do dicionário principal)
        """
        result = []
        for k in dic.keys():
            if k == "$":
                result = [*result, dic["$"]]
            else:
                result = [*result, *self.get_leafs_below(dic[k])]
        return result
        
        
    def find_pat(self, seq:str) -> list:
        """
        Devolve uma lista de índices onde se encontram a sequência especificada no padrão,
        ou 'False' caso não se encontre no padrão
        
        Parameters
        ----------
        :param seq: Uma sequência a ser procurada no padrão
        """
        dic = self.dic
        for s in seq:
            if s not in dic:
                print(f"'{seq}' não pertence à árvore de sufixos.")
                return False
            dic = dic[s]
        return self.get_leafs_below(dic)
    
x = SuffixTree("ABABBCAB")
print(x.find_pat("AB"))
print()
print(x)