# -*- coding: utf-8 -*-
"""
Created on Mon Feb 28 02:03:56 2022

@author: rober
"""

class Automato:
    
    def __init__(self, alphabet, pattern):
        self.alphabet = alphabet
        self.pattern = " " + pattern
        self.parts = [self.pattern[0:num] for num in range(1, len(self.pattern)+1)]
        self.mat = {num:{} for num in range(len(self.pattern))}
        self.transicoes()
        
        
    def new_state(self,key,part):
        
        state = 0
        for sub in [part[ind:] for ind in range(1,key+2)]:
            if " "+sub in self.parts:
                state = self.parts.index(" "+sub)
                self.mat[key][part[-1]] = state
                return True
            
        self.mat[key][part[-1]] = state
    
        
    def transicoes(self):
        
        for key in self.mat:
            for al in self.alphabet:
                
                if key != len(self.pattern)-1:
                    if al == self.pattern[key+1]:
                        self.mat[key][al] = key + 1
                    else:
                        part = self.parts[key] + al
                        self.new_state(key, part)
                        
                else:
                    self.new_state(key, self.pattern + al)
                    
        
    def af(self, texto):
        state = 0
        results = []
        for ind,elem in enumerate(texto):
            state = self.mat[state][elem]
            if state == len(self.pattern)-1:
                results.append( ind - len(self.pattern) + 2 )
        return results
    
    
    def print_automato(self):
        print("\t".join(["State", *self.alphabet]))
        for k in self.mat:
            line = [str(k)]
            for al in self.alphabet:
                line.append(str(self.mat[k][al]))
            print("\t".join(line))
                
        
alpha = "ACGT"                
pattern = "ACA"
seq = "TTTTACAACACACAAATGGAACA"


x = Automato(alpha, pattern)
print(x.af(seq))
print()
x.print_automato()