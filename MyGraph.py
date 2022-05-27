# -*- coding: utf-8 -*-

## Graph represented as adjacency list using a dictionary
## keys are vertices
## values of the dictionary represent the list of adjacent vertices of the key node

import math
from typing import Union

class MyGraph:
    
    """
    Classe que cria um grafo e efetua análises ao mesmo
    """
    
    def __init__(self, g:dict = {}, w = False):
        """
        Guarda os parâmetros importantes para a criação de grafos, definindo também o seu tipo
        
        Parameters
        ----------
        :param g: Dicionário que representa o grafo
        :param w: Booleano que indica se grafo tem pesos (True) ou não (False)
        """
        if type(g) !=dict:
            raise TypeError("O grafo deve ser do tipo dicionário")
        if type(w) != bool:
            raise TypeError("O weight deve ser do tipo boolean")

        self.graph = g
        #self.orig_graph = g #Guarda grafo original, caso sejam efetuadas alterações
        self.weighted = w #Define se grafo tem pesos ou não
        self._check_weights()
        
    def _check_weights(self):
        """
        Define todos os pesos como None no caso do grafo ser definido como não tendo pesos,
        e converte todos os valores de pesos não numéricos para 0 no caso de ser um grafo com pesos
        """
        for n1 in self.graph:
            for n2 in self.graph[n1]:
                if self.weighted == False:
                    self.graph[n1][n2] = None
                else:
                    if not type(self.graph[n1][n2]) in [int,float]:
                        self.change_weights(n1,n2,0) #Altera valor dos pesos para 0 quando o valor não-numérico é detetado
    
    
    def _check_valid(self, v:str) -> bool:
        """
        Verifica se um nodo está presente no grafo
        
        Parameters
        ----------
        :param v: Possível nodo no grafo
        """
        if v in self.graph:
            return True
        else:
            return False
        
    
    def change_type(self, w:bool):
        """
        Altera o tipo do grafo (define se tem pesos ou não)
        
        Parameters
        ----------
        :param w: Booleano que indica se grafo tem pesos (True) ou não (False)
        """

        if w==True:
            for n1 in self.graph:
                for n2 in self.graph[n1]:
                    if not type(self.graph[n1][n2]) in [int,float]:
                        self.graph[n1][n2] = 0 #Altera todos os valores não-numéricos para 0
            self.weighted = True
                        
        else:
            for n1 in self.graph:
                for n2 in self.graph[n1]:
                    self.graph[n1][n2] = None #Altera todos os valores dos pesos para None
            self.weighted = False
            
    
    def change_weights(self, node1:str, node2:str, value: Union[int,float,None]) -> bool:
        """
        Altera o peso de um determinado arco entre dois nodos
        
        Parameters
        ----------
        :param node1: Um nodo da ligação
        :param node2: Um nodo da ligação
        :param value: Valor do peso entre os nodos especificado
        """

        if (node1 in self.graph) and (node2 in self.graph) and (node2 in self.graph[node1]):
            self.graph[node1][node2] = value
            return True
        elif not self._check_valid(node1):
            print("'node1' does not exist in the graph")
            return False
        elif not self._check_valid(node2):
            print("'node2' does not exist in the graph")
            return False
        else:
            print("'node1' is not connected to 'node2'")
            return False
                

    def print_graph(self):
        """
        Imprime o grafo na forma de uma lista de adjacência
        """
        for v in self.graph.keys():
            if self.weighted:
                print (v, " -> ", self.graph[v])
            else:
                print (v, " -> ", list(self.graph[v]))
                
    # def print_orig_graph(self):
    #     """
    #     Imprime o grafo original (caso tenha ocorrido alterações na estrutura do mesmo)
    #     """
    #     self.temp = self.graph
    #     self.graph = self.orig_graph
    #     self.print_graph()
    #     self.graph = self.temp

    ## get basic info

    def get_nodes(self) -> list:
        """
        Devolve uma lista dos nodos do grafo
        """
        return list(self.graph.keys())
        
    
    def get_edges(self) -> list: 
        """
        Devolve uma lista dos arcos do grafo em forma de tuplos (origem, destino, peso (caso seja um grafo com pesos))
        """
        edges = []
        for v in self.graph.keys():
            for d in self.graph[v]:
                if self.weighted:
                    edges.append((v, d, self.graph[v][d]))
                else:
                    edges.append((v,d))
        return edges
      
        
    def size(self):
        """
        Devolve o tamanho do grafo: número de nodos, número de arcos
        """
        return len(self.get_nodes()), len(self.get_edges())
      
        
    ## add nodes and edges    
    
    def add_vertex(self, v:str):
        """
        Adiciona um vértice ao grafo, caso não tenha sido já adicionado
        
        Parameters
        ----------
        :param v: Nodo a adicionar ao grafo
        """
        if v not in self.graph:
            self.graph[v] = {}
        
        
    def add_edge(self, o:str, d:str, w: Union[int,float,None] = None):
        """
        Adiciona arco ao grafo, adicionando os nodos caso não existam
        
        Parameters
        ----------
        :param o: Nodo origem
        :param d: Nodo destino
        :param w: Peso associado ao arco
        """
        assert w==None or type(w) in [int,float], "Parâmetro 'w' deve ser NoneType ou um valor numérico"
        
        self.add_vertex(o)
        self.add_vertex(d)
        if w == None:
            #Caso o grafo tenha pesos, converte 'None' para 0
            val = w if self.weighted==False else 0
        else:
            #Caso grafo não tenha pesos, o valor de 'w' é convertido para 'None'
            val = None if self.weighted==False else w
        self.graph[o][d] = val



    ## successors, predecessors, adjacent nodes
    
    def get_successors(self, v:str) -> int:
        """
        Devolve lista dos sucessores do nodo especificado
        
        Parameters
        ----------
        :param v: Nodo do grafo
        """
        if not self._check_valid(v):
            return []
        else:
            return list(self.graph[v])
             
    
    def get_predecessors(self, v:str) -> list:
        """
        Devolve lista dos antecessores do nodo especificado
        
        Parameters
        ----------
        :param v: Nodo do grafo
        """
        res = []
        for k in self.graph:
            if v in self.graph[k]:
                res.append(k)
        return res
    
    
    def get_adjacents(self, v:str) -> list:
        """
        Devolve lista dos sucessores e antecessores do nodo especificado
        
        Parameters
        ----------
        :param v: Nodo do grafo
        """
        return list(set( self.get_successors(v) + self.get_predecessors(v) ))
        
    
    ## degrees    
    
    def out_degree(self, v:str) -> int:
        """
        Devolve o grau de saída do nodo especificado
        
        Parameters
        ----------
        :param v: Nodo do grafo
        """
        return len(self.get_successors(v))
    
    
    def in_degree(self, v:str) -> int:
        """
        Devolve o grau de entrada do nodo especificado
        
        Parameters
        ----------
        :param v: Nodo do grafo
        """
        return len(self.get_predecessors(v))
        
    
    def degree(self, v:str) -> int:
        """
        Devolve grau de entrada e saída do nodo especificado
        
        Parameters
        ----------
        :param v: Nodo do grafo
        """
        return len(self.get_adjacents(v))
        
    
    ## BFS and DFS searches    
    
    def reachable_bfs(self, v:str) -> list:
        """
        Devolve lista de nodos atingíveis através do nodo especificado
        (procura em largura)
        
        Parameters
        ----------
        :param v: Nodo do grafo
        """
        if not self._check_valid(v):
            return []
        else:
            l = [v]
            res = []
            while len(l) > 0:
                node = l.pop(0)
                if node != v: res.append(node)
                for elem in self.graph[node]:
                    if elem not in res and elem not in l and elem != node:
                        l.append(elem)
            return res
        
    def reachable_dfs(self, v:str) -> list:
        """
        Devolve lista de nodos atingíveis através do nodo especificado
        (procura em profundidade)
        
        Parameters
        ----------
        :param v: Nodo do grafo
        """
        if not self._check_valid(v):
            return []
        else:
            l = [v]
            res = []
            while len(l) > 0:
                node = l.pop(0)
                if node != v: res.append(node)
                s = 0
                for elem in self.graph[node]:
                    if elem not in res and elem not in l:
                        l.insert(s, elem)
                        s += 1
            return res    
    
    
    # distâncias
    
    def distance(self, o:str, d:str) -> Union[int,None]:
        """
        Devolve a distância entre 2 nodos
        
        Parameters
        ----------
        :param o: Nodo de origem
        :param d: Nodo de destino
        """
        if not self._check_valid(o):
            return None
        else:
            if o == d: return 0
            l = [(o,0)]
            visited = [o]
            while len(l) > 0:
                n1,dist = l.pop(0)
                for n2 in self.graph[n1]:
                    if n2 == d:
                        return dist + self.__dist(n1,n2)
                    elif n2 not in visited:
                        l.append((n2, dist + self.__dist(n1,n2)))
                        visited.append(n2)
            return None
    
    
    def shortest_path(self, o:str, d:str) -> Union[list,None]:
        """
        Devolve o caminho mais curto entre 2 nodos
        
        Parameters
        ----------
        :param o: Nodo de origem
        :param d: Nodo de destino
        """
        if self.weighted == False:
            return self._shortest_path(o,d)
        else:
            return self.dijkstra(o,d)
    
        
    def _shortest_path(self, o:str, d:str) -> Union[list,None]:
        """
        Devolve o caminho mais curto entre 2 nodos quando o grafo não tem pesos
        
        Parameters
        ----------
        :param o: Nodo de origem
        :param d: Nodo de destino
        """
        if not self._check_valid(o):
            return None
        else:
            if o == d: return [o,d]
            l = [(o, [o])]
            visited = [o]
            while len(l) > 0:
                n,path = l.pop(0)
                for node in self.graph[n]:
                    if node == d:
                        return path + [d]
                    elif node not in visited:
                        l.append((node,path+[node]))
                        visited.append(node)
            return None
    
    
    def __dist(self, prev:str, nxt:str) -> Union[int,float]:
        """
        Devolve a distância entre os nodos caso seja um grafo com pesos.
        Caso não seja, devolve 1
        
        Parameters
        ----------
        :param prev: Nodo prévio
        :param nxt: Nodo seguinte
        """
        if self.weighted == True:
            return self.graph[prev][nxt]
        else:
            return 1
        
        
    def _is_in_tuple_list(self, tuple_list:list, node:int) -> bool:
        """
        Método auxiliar de reachable_with_dist() que retorna True ou False dependendo de o nodo (que toma 
        como parâmetro) se encontrar na lista de tuplos ou não.

        Parameters
        ----------
        :param tuple_list: A lista de tuplos
        :param node: O nodo a procurar na lista de tuplos
        """
        for (x, y) in tuple_list:
            if node == x: return True
        return False
    
    
    def reachable_with_dist(self, o:str) -> list:
        """
        Devolve uma lista de tuplos contendo os nodos atingíveis e as suas respetivas distâncias
        a partir de um nodo de origem
        
        Parameters
        ----------
        :param o: Nodo de origem
        """
        
        res = []
        l = [(o,0)]
        while len(l) > 0:
            node, dist = l.pop(0)
            if node != o:
                res.append((node,dist))
            for elem in self.graph[node]:
                if not self._is_in_tuple_list(res, elem) and not self._is_in_tuple_list(l, elem):
                    l.append((elem, dist + self.__dist(node, elem)))
        return res
    
    # DIJKSTRA (Geração do grafo de dijkstra e determinação do caminho mais curto entre 2 nodos)
    
    def __get_mins(self, distances:dict) -> tuple:
        """
        Método auxiliar de dijkstra() que retorna um tuplo com os valores da menor distância e os nodos para os quais 
        esta se verifica.
        
        Parameters
        ----------
        :param distances: Dicionário de distâncias
        """
        min_dist = math.inf
        prev_node = min_node = 0
        for node in distances:
            for k in distances[node]:
                if distances[node][k] < min_dist:
                    prev_node = node
                    min_node = k
                    min_dist = distances[node][k]
        return prev_node, min_node, min_dist


    def __get_path(self, djkstr:dict, o:int, d:int) -> str:
        """
		Método auxiliar de dijkstra() que retorna o caminho mais curto entre o nodo de origem e o nodo de destino
		de forma legível.

		Parameters
		----------
		:param djkstr: O dicionário de distâncias
		:param o: Nodo de origem
		:param d: Nodo de destino
		"""
        node = d
        path = [str(d)]
        while node != o:
            node = djkstr[node][0]
            path.insert(0, str(node))
        return " -> ".join(path) + f" (dist = {djkstr[d][1]})"

    
    def dijkstra(self, o:int, d:int) -> str:
        """
		Devolve o caminho mais curto entre 2 nodos implmentando do algoritmo de Dijkstra
        (quando o grafo tem pesos)

		Parameters
		----------
		:param o: Nodo de origem
		:param d: Nodo de destino
		"""  
        if not self._check_valid(o) or not self._check_valid(d):
            return None
        else:
            djkstr = {k: [0, 0] for k in self.graph} # djkstr[k][0] -> proveniência; djkstr[k][1] -> distância ao nodo inicial
            marked = [o]
            while d not in marked and len(marked) != len(self.graph):
                distances = {}
                for node in marked:
                    distances[node] = {}
                    for k in self.graph[node]:
                        if k not in marked: # de modo a não incluír como destino nodos já marcados no dicionário de distâncias
                            distances[node][k] = self.__dist(node,k) + djkstr[node][1]
                            prev_node, min_node, min_dist = self.__get_mins(distances)
                marked += [min_node]
                djkstr[min_node][0] = prev_node
                djkstr[min_node][1] = min_dist
            if d in marked:
                return self.__get_path(djkstr, o, d)
            else:
                return False



#     def __get_mins(self, dist:int, nxt_list:list) -> tuple:
#         """
#         Método auxiliar de dijkstra() que retorna um tuplo com os valores da menor distância e os nodos para os quais 
#         esta se verifica.
        
#         Parameters
#         ----------
#         :param distances: Dicionário de distâncias
#         """
#         res = []
#         print(nxt_list)
#         for nxt,prev,d in nxt_list:
#             new_dist = dist + self.graph[prev][nxt]
#             print(prev,nxt,new_dist)
#             if new_dist < d:
#                 res.append((nxt,prev,new_dist))
#         return sorted(res, key = lambda x: x[2])


#     def __get_path(self, djkstr:dict, o:int, d:int) -> str:
#         """
# 		Método auxiliar de dijkstra() que retorna o caminho mais curto entre o nodo de origem e o nodo de destino
# 		de forma legível.

# 		Parameters
# 		----------
# 		:param djkstr: O dicionário de distâncias
# 		:param o: Nodo de origem
# 		:param d: Nodo de destino
# 		"""
#         node = d
#         path = [str(d)]
#         while node != o:
#             node = djkstr[node][0]
#             path.insert(0, str(node))
#         return path
    
    
#     def dijkstra(self, o:int, d:int) -> list:
#         """
# 		Devolve o caminho mais curto entre 2 nodos implmentando do algoritmo de Dijkstra
#         (quando o grafo tem pesos)

# 		Parameters
# 		----------
# 		:param o: Nodo de origem
# 		:param d: Nodo de destino
# 		"""
#         if not self._check_valid(o) or not self._check_valid(d):
#             print("Caminho inválido")
#             return []
#         else:
#             djkstr = {k: ["", 0] for k in self.graph} # djkstr[k][0] -> nodo anterior; djkstr[k][1] -> distância ao nodo inicial
#             nxt = [(o,o,0)] #Lista ordenada de valores por avaliar (nodo, nodo anterior, distância ao nodo inicial)
#             checked = [o] #Valores já avaliados
#             while len(nxt) != 0:
#                 node,prev,dist = nxt.pop(0)
#                 djkstr[node] = [prev, dist]
                
#                 if node == d:
#                     return self.__get_path(djkstr, o, d)
                
#                 temp = [elem[0] for elem in nxt] #Para retirar apenas os nodos da lista de tuplos
#                 new_elems = [ (k, node, math.inf) for k in self.graph[node] if k not in [*checked] ]
#                 nxt += self.__get_mins(dist, new_elems)
#                 nxt = sorted(nxt, key = lambda x: x[2])
#                 checked.append(node)
#             return []
        
    
    
    

## cycles
    def node_has_cycle (self, v:str) -> bool:
        """
        Verifica se um nodo tem um caminho que forma um ciclo
        
        Parameters
        ----------
        :param v: Nodo do grafo
        """
        if v not in self.graph:
            return False
        l = [v]
        visited = [v]
        while len(l) > 0:
            node = l.pop(0)
            for elem in self.graph[node]:
                if elem == v: return True
                elif elem not in visited:
                    l.append(elem)
                    visited.append(elem)
        return False

    def has_cycle(self) -> bool:
        """
        Verifica se o grafo tem algum caminho que forma um ciclo
        """
        for v in self.graph.keys():
            if self.node_has_cycle(v): return True
        return False



# def is_in_tuple_list (tl, val):
#     res = False
#     for (x,y) in tl:
#         if val == x: return True
#     return res


def test1():
    gr = MyGraph( {1:{2:0}, 2:{3:3}, 3:{2:1,4:2}, 4:{2:0}}, w=True )
    print(gr.graph)
    # gr.print_graph()
    # print (gr.get_nodes())
    # print (gr.get_edges())
    # gr.dijkstra_distance(2, 4)
    # gr.add_vertex(5)


    

def test2():
    gr2 = MyGraph(w=True)
    gr2.add_vertex(1)
    gr2.add_vertex(2)
    gr2.add_vertex(3)
    gr2.add_vertex(4)
    
    gr2.add_edge(1,2)
    gr2.add_edge(2,3)
    gr2.add_edge(3,2)
    gr2.add_edge(3,4)
    gr2.add_edge(4,2)
    
    gr2.print_graph()
  
def test3():
    gr = MyGraph({1:{2:0}, 2:{3:0}, 3:{2:0,4:0}, 4:{2:0}})
    gr.print_graph()

    # print (gr.get_successors(2))
    # print (gr.get_predecessors(2))
    print (gr.get_adjacents(2))
    print (gr.in_degree(2))
    print (gr.out_degree(2))
    print (gr.degree(2))

def test4():
    # gr = MyGraph( {1:{2:0}, 2:{3:3}, 3:{2:1,4:2}, 4:{2:0}}, w=True )
    
    # print (gr.distance(1,4))
    # print (gr.distance(4,3))

    # print (gr.shortest_path(1,4))
    # print (gr.shortest_path(4,3))

    # # print (gr.reachable_with_dist(1))
    # # print (gr.reachable_with_dist(3))

    gr2 = MyGraph( {1:{2:0}, 2:{3:0}, 3:{2:0,4:0}, 4:{2:0}} )
    
    print (gr2.distance(2,1))
    print (gr2.distance(1,5))
    
    print (gr2.shortest_path(1,4))
    print (gr2.shortest_path(2,1))

    print (gr2.reachable_with_dist(1))
    # print (gr2.reachable_with_dist(5))

def test5():
    gr = MyGraph( {1:{2:0}, 2:{3:0}, 3:{2:0,4:0}, 4:{2:0}} )
    print (gr.node_has_cycle(2))
    print (gr. node_has_cycle(1))
    print (gr.has_cycle())

    # gr2 = MyGraph( {1:[2,3], 2:[4], 3:[5], 4:[], 5:[]} )
    # print (gr2. node_has_cycle(1))
    # print (gr2.has_cycle())
    
    
def test6():
    gr = MyGraph( {1:{2:2, 3:5}, 2:{1:2, 3:3, 4:1, 5:2}, 3:{1:5, 2:3, 4:1, 5:2},
                   4:{2:1, 3:1, 5:2, 6:7}, 5:{2:2, 3:2, 4:2, 6:3}, 6:{4:7, 5:3}}, w=True)
    
    print(gr.shortest_path(1, 6))


if __name__ == "__main__":
    #test1()
    #test2()
    #test3()
    test4()
    #test5()
    #test6()
