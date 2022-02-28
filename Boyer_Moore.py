# -*- coding: utf-8 -*-
"""
Created on Mon Feb 28 02:02:52 2022

@author: rober
"""

import re

class BoyerMoore:
    
    def __init__(self,alphabet,pattern):
        self.alpha = alphabet
        self.pat = pattern
        
        self.bcr()
        self.gsr()
        
    
    def bcr(self):
        
        self.salto_bcr = {ind:{} for ind in range(len(self.pat))}
        
        for letter in self.alpha:
            self.salto_bcr[0][letter] = 1
            
            for ind in range(1,len(self.pat)):
                
                #Vai buscar a última ocorrência da letra na subsequência
                pos = ind - self.pat[0:ind][::-1].find(letter)
                
                if pos > ind: #Quer dizer que não foi encontrado o elemento (ind - (-1))
                    self.salto_bcr[ind][letter] = ind + 1
                else:
                    self.salto_bcr[ind][letter] = ind - pos + 1
                    
    
    def gsr(self):
        
        self.salto_gsr = {self.pat[ind:] : 0 for ind in range(1,len(self.pat))}
        
        for ind,sub in enumerate(self.salto_gsr):
            fragmentos = [sub[i:] for i in range(len(sub))]
            salto = len(self.pat)
            
            for frag in fragmentos:
                dots = "."*len(frag)
                check_list = re.findall(fr"(?=({dots}))", self.pat)
                check_list = check_list[:-1-(len(sub)-len(frag))] #Excluir os que estão apenas contidos no match inteiro
                if frag in check_list:
                    salto = check_list[::-1].index(frag) + len(sub) - len(frag) + 1 #Para alinhar com a correspondência
                    break
                    
            self.salto_gsr[sub] = salto
            
                
                
    def procura(self,texto):
        
        dots = "."*len(self.pat)
        subseqs = re.findall(fr"(?=({dots}))", texto)
        results = []
        ind = 0
        while ind < len(subseqs):
            if subseqs[ind] == self.pat:
                results.append(ind)
                ind += len(self.pat)
            else:
                mismatch = len(self.pat)-1
                while self.pat[mismatch] == subseqs[ind][mismatch]:
                    mismatch -= 1
                
                letra = subseqs[ind][mismatch]
                if mismatch == len(self.pat)-1:
                    ind += self.salto_bcr[mismatch][letra]
                else:
                    suffix = subseqs[ind][mismatch+1:]
                    ind += max(self.salto_bcr[mismatch][letra], self.salto_gsr[suffix])
                    
        return results
            
        
        
        
            

a='ATCG'
p='ATTTTG'
p="A"
B=BoyerMoore(a,p) 
print(B.procura('ATATATGGGTGATTTTGGGTAATTTTG'))