# -*- coding: utf-8 -*-

def createMatpwm(nl:int, nc:int, pseudo: float=1)->list:
    """
    Devolve uma matriz consoante o tamanho das sequência e o tamanho do alfabeto
        
    Parameters
    ----------
    :param nl: tamanho da sequência
    :param nc: tamanho do dicionário
    :pseudocontagem
    """
    res = []
    for i in range(0, nl):
        res.append([pseudo]*nc)
    return res 

def printMat(mat:list):
    """
    Devolve a matriz formatada 
    """
    for i in range(0, len(mat)): print(mat[i])

        
        
"""
Class: MyMotif
"""

class MyMotifs:

    def __init__(self, seqs:object, pseudo:float=0):
        """
        Recebe objeto(lista de seqências) e pseudocontagem

        Parameters
        ----------
        :param seqs: objeto de lista de sequências
        :param pseudo: pseudocontagem
        """
        self.size = len(seqs[0])
        self.seqs = seqs # objetos classe MySeq
        self.alphabet = seqs[0].alfabeto()
        self.createPWM(pseudo)
        self.doCounts(pseudo)
    
    
    def __len__ (self)->int:
        """
        Devolve cumprimento da 1ª sequência
        """
        return self.size 
    
    
    def doCounts(self, pseudo:float=0):
        """
        Cria matriz tendo em conta a pseudocontagem
        
        Parameters
        ----------
        :param pseudo: pseudocontagem
        """
        self.counts = createMatpwm(len(self.alphabet), self.size, pseudo) #Utilização da função que cria uma matriz de segundo pseudo
        for s in self.seqs:
            for i in range(self.size):
                lin = self.alphabet.index(s[i])
                self.counts[lin][i] += 1

                
    def createPWM(self, pseudo:float = 0):
        """
        Cria matriz PWM tendo em conta a pseudocontagem
        
        Parameters
        ----------
        :param pseudo: Pseudocontagem
        """
        self.doCounts(pseudo)
        for i in range(len(self.alphabet)):
            for j in range(self.size):
                self.counts[i][j] = float(self.counts[i][j]) / (len(self.seqs) + len(self.alphabet)* pseudo)
  
                
    def consensus(self)->str:
        """
        Devolve o consenso entre as seqências
        """
        res = ""
        for j in range(self.size):
            maxcol = self.counts[0][j]
            maxcoli = 0
            for i in range(1, len(self.alphabet) ):
                if self.counts[i][j] > maxcol: 
                    maxcol = self.counts[i][j]
                    maxcoli = i
            res += self.alphabet[maxcoli]        
        return res

    def maskedConsensus(self)->str:
        """
        Devolve as posições mais significantes, truncando as menos significantes
        (tendo em conta a quantidade de sequências)
        """
        res = ""
        for j in range(self.size):
            maxcol = self.counts[0][j]
            maxcoli = 0
            for i in range(1, len(self.alphabet) ):
                if self.counts[i][j] > maxcol: 
                    maxcol = self.counts[i][j]
                    maxcoli = i
            if maxcol > len(self.seqs) / 2:
                res += self.alphabet[maxcoli]        
            else:
                res += "-"
        return res

    def probabSeq (self, seq:str)->float:
        """
        Devolve a probabilidade da sequência especificada ser encontrada
        
        Parameters
        ----------
        :param seq: sequência
        """
        res = 1.0
        for i in range(self.size):
            lin = self.alphabet.index(seq[i])
            res *= self.counts[lin][i]
        return res
    
    def probAllPositions(self, seq:str)->list:
        """
        Devolve uma lista das probabilidades dos fragmentos da sequência especificada
        
        Parameters
        ----------
        :param seq: sequência
        """
        res = []
        for k in range(len(seq)-self.size+1):
            res.append(self.probabSeq(seq))
        return res

    def mostProbableSeq(self, seq:str)->int:
        """
        Devolve o indice da sequência especificada que mais se assemelha às fornecidas
        
        Parameters
        ----------
        :param seq: sequência
        """
        maximo = -1.0
        maxind = -1
        for k in range(len(seq)-self.size+1):
            p = self.probabSeq(seq[k:k+ self.size])
            if(p > maximo):
                maximo = p
                maxind = k
        return maxind
    
