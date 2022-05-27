"""
Class: BoyerMoore
"""

import re

class BoyerMoore:
    """
    Implementa o algoritmo de Boyer-Moore para a procura de padrões em
    sequências
    """
    
    def __init__(self, alphabet:str, pattern:str):
        """
        Gurada o alphabeto e padrão introduzidos, e chama os métodos 'bcr' e 'gsr'
        
        Parameters
        ----------
        :param alphabet: O alphabeto utilizado no padrão e texto a processar
        :param pattern: O padrão a ser procurado no texto
        """
        assert all(elem in alphabet for elem in set(pattern.upper())), "Padrão contém elementos não presentes no alphabeto"
        assert len(pattern) > 0, "Padrão tem de ter tamanho > 0"

        self.alpha = "".join(set(alphabet.upper()))
        self.pat = pattern.upper()
        
        self.bcr()
        self.gsr()
        #print(self.salto_bcr)
        #print()
        #print(self.salto_gsr)
        
    
    
    
    def bcr(self):
        """
        Implementa o 'Bad Character Rule' e prepara um dicionário de deslocações
        para cada posição do padrão definido
        """
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
        """
        Implementa o 'Good Suffix Rule' e prepara um dicionário de deslocações
        para cada posição do padrão definido
        """
        self.salto_gsr = {self.pat[ind:] : 0 for ind in range(1,len(self.pat))}
        
        for sub in self.salto_gsr:
            fragmentos = [sub[i:] for i in range(len(sub))]
            salto = len(self.pat)
            
            for frag in fragmentos:
                dots = "."*len(frag)
                check_list = re.findall(fr"(?=({dots}))", self.pat)
                check_list = check_list[:-1]
                if frag in check_list:
                    salto = check_list[::-1].index(frag) + len(sub) - len(frag) + 1 #Para alinhar com a correspondência
                    break
                    
            self.salto_gsr[sub] = salto
            
                
                
    def procura(self, texto:str, pat_in_pat:bool = True) -> list:
        """
        Devolve uma lista de índices do texto onde foram encontrados correspondências
        exatas do padrão.
        
        Parameters
        ----------
        :param texto: String onde se pretende procurar ocorrências do padrão
        :param pat_in_pat: Booleano que indica se se deve procurar o padrão quando se sobrepõe
        """
        assert all(elem in self.alpha for elem in set(texto.upper())), "Parâmetro 'texto' contém elementos não presentes no alphabeto" 
        
        dots = "."*len(self.pat)
        subseqs = re.findall(fr"(?=({dots}))", texto.upper())
        results = []
        ind = 0
        while ind < len(subseqs):
            if subseqs[ind] == self.pat:
                results.append(ind)
                if pat_in_pat:
                    ind += 1
                else:
                    ind += len(self.pat)
            else:
                mismatch = len(self.pat)-1
                while self.pat[mismatch] == subseqs[ind][mismatch]:
                    mismatch -= 1
                
                letra = subseqs[ind][mismatch]
                if mismatch == len(self.pat)-1: #Não existe "Good Suffix" neste caso
                    ind += self.salto_bcr[mismatch][letra]
                else:
                    suffix = subseqs[ind][mismatch+1:]
                    ind += max(self.salto_bcr[mismatch][letra], self.salto_gsr[suffix])
                    
        return results
