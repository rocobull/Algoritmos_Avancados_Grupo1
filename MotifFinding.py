# -*- coding: utf-8 -*-

"""
Class: MotifFinding
"""

from MySeq import MySeq
from MyMotifs import MyMotifs
import random

class MotifFinding:
    """
    Implementa 2 tipos(heuristico e heuristico estocástico)  de procura de motifs, por consensus.
    """
    
    def __init__(self, size: int = 8, seqs: list = None):
        """
        Guarda o tamanho do motif que está a ser procurado e as sequências fornecidas.

        Parameters
        ----------
        :param size: Tamanho do motif procurado, O default é 8.
        :param seqs: Lista de objetos com as sequências (str).
        """
        self.motifSize = size
        if (seqs != None):
            self.seqs = seqs
            self.alphabet = seqs[0].alfabeto()
        else:
            self.seqs = []
                    
    def __len__ (self) -> int: 
        """
        Retorna o número de sequências.
        """
        return len(self.seqs)
    
    def __getitem__(self, n:int) -> int:
        """
        Retorna a seqência segundo a sua posição na lista de sequências.
        
        Parameters
        ----------
        :param n: indice da sequência na lista.
        """
        return self.seqs[n]
    
    def seqSize (self, i:int) -> int:
        """
        Retorna o tamanho da seqência segundo a sua posição na lista de sequências.
        
        Parameters
        ----------
        :param i: indice da sequência na lista.
        """
        return len(self.seqs[i])
    
    def readFile(self, fic:str, t:str):
        """
        Lê file com sequências, tendo em conta o alfabeto utilizado.
        
        Parameters
        ----------
        :param fic: localização do ficheiro
        :param t: alfabeto
        """
        for s in open(fic, "r"):
            self.seqs.append(MySeq(s.strip().upper(),t))
        self.alphabet = self.seqs[0].alfabeto()
        
    def createMotifFromIndexes(self, indexes:list)-> object:
        """
        Extrai os Motifs a partir dos indices.
        
        Parameters
        ----------
        :param indexes: lista com indices do incio dos motifs nas sequencias
        """
        pseqs = []
        for i,ind in enumerate(indexes):
            pseqs.append( MySeq(self.seqs[i][ind:(ind+self.motifSize)], self.seqs[i].tipo) )
        return MyMotifs(pseqs)
    
    def score(self, s:list, pseudo:float = 0) -> int:
        """
        Devolve score relativo às posições do motif fornecidas na lista.
        
        Parameters
        ----------
        :param s: indices do incio do motif nas sequencias
        :param pseudo: pseudocontagem no calculo do score
        """
        
        score = 0
        motif = self.createMotifFromIndexes(s)
        
        motif.doCounts(pseudo)
        mat = motif.counts
        for j in range(len(mat[0])):
            maxcol = mat[0][j]
            for  i in range(1, len(mat)):
                if mat[i][j] > maxcol: 
                    maxcol = mat[i][j]
            score += maxcol
       
        return score
        
    
    def scoreMult(self, s, pseudo:float=0) -> float:
        """
        Devolve score proabilistico segundo o pwm, relativo às posições do motif fornecidas na lista
        
        Parameters
        ----------
        :param s: indices do incio do motif nas sequencias
        :param option: Caso seja ='pseudo', realiza a criação da pwm com pseudocontagem
        """
        score = 1.0
        motif = self.createMotifFromIndexes(s)
        motif.createPWM(pseudo)
        mat=motif.counts
        for j in range(len(mat[0])):
            maxcol = mat[0][j]
            for  i in range(1, len(mat)):
                if mat[i][j] > maxcol: 
                    maxcol = mat[i][j]
            score *= maxcol
        return score
    
    
    def nextSol (self, s:list) ->list:
        """
        Devolve lista com indices para a realização da procura exaustiva
        
        Parameters
        ----------
        :param s: indices do incio do motif nas sequencias
        """
        nextS = [0]*len(s)
        pos = len(s) - 1     
        while pos >=0 and s[pos] == self.seqSize(pos) - self.motifSize:
            pos -= 1
        if (pos < 0): 
            nextS = None
        else:
            for i in range(pos): 
                nextS[i] = s[i]
            nextS[pos] = s[pos]+1;
            for i in range(pos+1, len(s)):
                nextS[i] = 0
        return nextS
                   
    def exhaustiveSearch(self) -> list:
        """
        Rertorna indices com melhores scores correspondestes ao inicio dos motifs
        """
        melhorScore = -1
        res = []
        s = [0]* len(self.seqs)
        while (s!= None):
            sc = self.score(s)
            if (sc > melhorScore):
                melhorScore = sc
                res = s
            s = self.nextSol(s)
    
        return res
    
    def re_motif(self, indx:list)->list:
        """
        Devolve lista dos motifs segundo os indices fornecidos
        
        Parameters
        ----------
        :param indx: indices do incio do motif nas sequencias
        """
        tam = self.motifSize
        lista_seq = self.seqs
        return [lista_seq[i][indx[i]:indx[i]+tam] for i in range(len(lista_seq))]
    
    def nextVertex (self, s):
        """
        Devolve lista dos indices de cada folha para cada vertice da árvore de procura
        
        Parameters
        ----------
        :param s: lista de indices para o inicio de cada motif
        """
      
        res =  []
        if len(s) < len(self.seqs): # internal node -> down one level
            for i in range(len(s)): 
                res.append(s[i])
            res.append(0)
        else: # bypass
            pos = len(s)-1 
            while pos >=0 and s[pos] == self.seqSize(pos) - self.motifSize:
                pos -= 1
            if pos < 0: res = None # last solution
            else:
                for i in range(pos): res.append(s[i])
                res.append(s[pos]+1)
        return res
    
    
    def bypass (self, s):
        """
        Verifica que as folhas do vértice atual não têm melhor solução e passa para o vértice seguinte
        
        Parameters
        ----------
        :param s: lista de indices para o inicio de cada motif
        """
        
        res =  []
        pos = len(s) -1
        while pos >=0 and s[pos] == self.seqSize(pos) - self.motifSize:
            pos -= 1
        if pos < 0: res = None 
        else:
            for i in range(pos): res.append(s[i])
            res.append(s[pos]+1)

        return res
        
    def branchAndBound (self):
        """
        Devolve lista dos indices de inicio dos motifs aplicando o método branch and bound
        """
        melhorScore = -1
        melhorMotif = None
        size = len(self.seqs)
        s = [0]*size
        while s != None:
            if len(s) < size:
                optimScore = self.score(s) + (size-len(s)) * self.motifSize
                if optimScore < melhorScore: s = self.bypass(s)
                else: s = self.nextVertex(s)
            else:
                sc = self.score(s)
                if sc > melhorScore:
                    melhorScore = sc
                    melhorMotif  = s
                s = self.nextVertex(s)
        return melhorMotif
        
    
    def Heuristic(self)->list:
        """
        Realiza procura heuristica dos motifs utilizando o consensus, 
        tendo incialmente em conta as duas primeiras sequências fornecidas.
        Devolvendo os indices para o motif encontrado nas sequências
        """
        # Considerando apenas as duas primeiras sequências, escolher as 
        # posições iniciais s1 e s2 que dão um melhor score
        # procura exaustiva nas duas primeiras sequências
        MC = MotifFinding(self.motifSize, self.seqs[:2])
        s = MC.exhaustiveSearch()
        #obtem-se os indices dos motifs das 2 primeiras seq
        #Para cada uma das sequências seguintes (i=3, …,t), 
        #escolher a melhor posição inicial na sequência i, de forma a 
        #maximizar o score
        for i in range(2,len(self.seqs)):
            s.append(0)
            score = -1
            pos = 0
            for j in range(self.seqSize(i)-self.motifSize+1):
                s[i] = j
                score_atual = self.score(s)
                if score_atual > score:
                    score = score_atual
                    pos = j
                s[i] = pos
                
        return s
    
    
    def HeuristicStochastic (self, pseudo:float = 0)->list:
        """
        Realiza procura heuristica estocástica dos motifs, tendo incialmente 
        em conta posiçoes aleatórias para o incio dos motifs.
        Devolvendo os indices para o motif encontrado nas sequências
 
        Parameters
        ----------
        :param s: indices do incio do motif nas sequencias
        :param pseudo: utiliza-se pseudocontagem (pwm)
        """

        num_seq = len(self.seqs)
        s=[]
        s.extend([0] * (num_seq))
        #Iniciar todas as posições com valores aleatórios
        for index in range(len(self.seqs)):
            #randint(A,B) =>"Random number between A and B"
            s[index] = random.randint(0, self.seqSize(index)-self.motifSize)
        #passo2
        melhor_score = self.score(s, pseudo)
        melhorar_s = True
        while melhorar_s:
            #constroi o perfil com base nas posições iniciais s
            motif = self.createMotifFromIndexes(s)
            motif.createPWM(pseudo)
            #avalia a melhor posição inicial para cada sequência com base no perfil
            for index in range(len(self.seqs)):
                s[index] = motif.mostProbableSeq(self.seqs[index])
            #caso exista melhoria, atualiza o score
            aval = self.score(s, pseudo)
            if aval > melhor_score:
                melhor_score = aval
            else:
                melhorar_s = False
        return s
