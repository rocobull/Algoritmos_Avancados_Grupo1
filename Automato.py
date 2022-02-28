# -*- coding: utf-8 -*-
"""
Created on Mon Feb 28 02:03:56 2022

@author: rober
"""

"""
Class: Automato
"""



class Automato:
    """
    Implementa um Automato finito para a procura de padrões em sequências
    """
    
    def __init__(self, alphabet:str, pattern:str):
        """
        Guarda os valores a serem utilizados pelos restantes métodos, e chama
        o método 'transicoes'
        
        Parameters
        ----------
        :param alphabet: O alphabeto utilizado no padrão e texto a processar
        
        :param pattern: O padrão a ser procurado no texto
        """
        self.alphabet = alphabet.upper()
        self.pattern = " " + pattern.upper()
        self.parts = [self.pattern[0:num] for num in range(1, len(self.pattern)+1)]
        self.mat = {num:{} for num in range(len(self.pattern))}
        self.transicoes()
        
        
    def new_state(self, key:int, part:str):
        """
        Define o novo estado do automato quando for encontrado um determinado
        padrão
        
        Parameters
        ----------
        :param key: A chave correspondente ao estado do automato no dicionário
                    de mudanças de estado
        
        :param part: Um padrão encontrado num determinado estado
        """
        state = 0
        for sub in [part[ind:] for ind in range(1,key+2)]:
            if " "+sub in self.parts:
                state = self.parts.index(" "+sub)
                self.mat[key][part[-1]] = state
                return True
            
        self.mat[key][part[-1]] = state
    
        
    def transicoes(self):
        """
        Constrói um dicionário de deslocações de estado para cada possível
        caractere encontrado em cada estado
        """
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
                    
        
    def af(self, texto:str) -> list:
        """
        Devolve uma lista de índices do texto onde foram encontrados correspondências
        exatas do padrão.
        
        Parameters
        ----------
        :param text: String onde se pretende procurar ocorrências do padrão
        """
        state = 0
        results = []
        for ind,elem in enumerate(texto.upper()):
            state = self.mat[state][elem]
            if state == len(self.pattern)-1:
                results.append( ind - len(self.pattern) + 2 )
        return results
    
    
    def print_automato(self):
        """
        Imprime o Automato de forma legível (matriz)
        """
        print("\t".join(["State", *self.alphabet]))
        for k in self.mat:
            line = [str(k)]
            for al in self.alphabet:
                line.append(str(self.mat[k][al]))
            print(line[0] + "\t\t" + "\t".join(line[1:]))
                
        
alpha = "ACGT"                
pattern = "ACA"
seq = "TTTTACAACACACAAATGGAACA"


x = Automato(alpha, pattern)
print(x.af(seq))
print()
x.print_automato()