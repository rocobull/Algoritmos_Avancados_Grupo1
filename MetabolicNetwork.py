# -*- coding: utf-8 -*-

from MyGraph import MyGraph

"""
Class: MetabolicNetwork
"""

class MetabolicNetwork (MyGraph):
    """
    Classe que guarda redes metabólicas em estruturas de grafos
    """
    
    def __init__(self, network_type:str = "metabolite-reaction", split_rev:bool = False):
        """
        Guarda as variáveis a serem utilizadas pela classe
        
        Parameters
        ----------
        :param network_type: String que define o tipo de rede metabólica a ser representada
        :param split_rev: Booleano que define se as reações reversíveis são consideradas como 2 reações distintas ou não
        """
        assert network_type.lower() in ["metabolite-reaction", "metabolite-metabolite", "reaction-reaction"],\
            "Parâmetro ´network_type' tem de ser 'metabolite-reaction', 'metabolite-metabolite' ou 'reaction-reaction'"
        
        MyGraph.__init__(self, {})
        self.net_type = network_type.lower()
        
        self.node_types = {}
        for tp in network_type.lower().split("-"):
            self.node_types[tp] = []
        self.split_rev =  split_rev
    
    
    def add_vertex_type(self, v:str, nodetype:str = None):
        """
        Adicionar um nodo de um determinado tipo no grafo
        
        Parameters
        ----------
        :param v: Nodo a ser inserido no grafo
        :param nodetype: Tipo do nodo ('metabolite' ou 'reaction')
        """
        if type(nodetype) == str:
            nodetype = nodetype.lower()
        assert nodetype in ['metabolite','reaction',None], "Parâmetro 'nodetype' tem de ser 'metabolite' ou 'reaction'"
        
        if nodetype == None:
            if self.net_type == "metabolite-metabolite":
                nodetype = "metabolite"
            elif self.net_type == "reaction-reaction":
                nodetype = "reaction"
            else:
                raise AttributeError("Parâmetro 'nodetype' não pode ser 'None'\
                                     quando o grafo é do tipo 'metabolite-reaction'.\
                                         É preciso especificar o tipo do nodo")
        
        #Para garantir que não haja repetições de valores entre metabolitos e reações
        all_vals = []
        for vals in self.node_types.values():
            all_vals.extend(vals)
        
        if (v not in all_vals) and (v != ""): #Não aceita valores vazios
            self.node_types[nodetype].append(v)
            self.add_vertex(v)
    
    
    def get_nodes_type(self, node_type:str = None) -> list:
        """
        Devolve uma lista com os nodos do tipo especificado.
        Se não for especificado um tipo, devolve a lista dos nodos
        correspondentes ao tipo do grafo.
        No caso de ser do tipo 'metabolite-reaction', devolve uma lista de listas
        com os dois tipos, na ordem: [[metabolitos], [reações]]
        
        Parameters
        ----------
        :param node_type: Tipo do nodo ('metabolite', 'reaction' ou 'metabolite-reaction')
        """        
        if node_type == None:
            if self.net_type == "metabolite-metabolite":
                return self.node_types["metabolite"]
            elif self.net_type == "reaction-reaction":
                return self.node_types["reaction"]
            else:
                return [self.node_types["metabolite"], self.node_types["reaction"]]
        
        else:
            return self.node_types[node_type]
    
    
    def load_from_file(self, filename:str):
        """
        Cria um grafo metabólico a partir de um ficheiro contendo reações metabólicas
        em cada linha
        
        Parameters
        ----------
        :param filename: Nome do ficheiro contendo reações metabólicas
        """
        rf = open(filename)
        gmr = MetabolicNetwork("metabolite-reaction")
        for line in rf:
            if ":" in line:
                tokens = line.split(":")
                reac_id = tokens[0].strip()
                gmr.add_vertex_type(reac_id, "reaction")
                rline = tokens[1]
            else: raise Exception("Invalid line:")                
            if "<=>" in rline:
                left, right = rline.split("<=>")
                mets_left = left.split("+")
                for met in mets_left:
                    met_id = met.strip()
                    gmr.add_vertex_type(met_id, "metabolite")
                    if self.split_rev:
                        gmr.add_vertex_type(reac_id+"_b", "reaction")
                        gmr.add_edge(met_id, reac_id)
                        gmr.add_edge(reac_id+"_b", met_id)
                    else:
                        gmr.add_edge(met_id, reac_id)
                        gmr.add_edge(reac_id, met_id)
                mets_right = right.split("+")
                for met in mets_right:
                    met_id = met.strip()
                    gmr.add_vertex_type(met_id, "metabolite")
                    if self.split_rev:
                        gmr.add_edge(met_id, reac_id+"_b")
                        gmr.add_edge(reac_id, met_id)
                    else:
                        gmr.add_edge(met_id, reac_id)
                        gmr.add_edge(reac_id, met_id)
                        
            elif "=>" in line:
                left, right = rline.split("=>")
                mets_left = left.split("+")
                for met in mets_left:
                    met_id = met.strip()
                    gmr.add_vertex_type(met_id, "metabolite")
                    gmr.add_edge(met_id, reac_id)
                mets_right = right.split("+")
                for met in mets_right:
                    met_id = met.strip()
                    gmr.add_vertex_type(met_id, "metabolite")
                    gmr.add_edge(reac_id, met_id)
            else: raise Exception("Invalid line:")    

        if self.net_type == "metabolite-reaction":
            self.graph = gmr.graph
        elif self.net_type == "metabolite-metabolite":
            self._convert_metabolite_net(gmr)
        else:
            self._convert_reaction_graph(gmr)
        
        self.node_types = gmr.node_types
        
        
    def _convert_metabolite_net(self, gmr:dict):
        """
        Converte grafo do tipo 'metabolite-reaction' para 'metabolite-metabolite'
        
        Parameters
        ----------
        :param gmr: Grafo a converter
        """
        for m in gmr.node_types["metabolite"]:
            self.add_vertex(m)
            sucs = gmr.get_successors(m)
            for s in sucs:
                sucs_r = gmr.get_successors(s)
                for s2 in sucs_r:
                    if m != s2: self.add_edge(m, s2) 

        
    def _convert_reaction_graph(self, gmr:dict): 
        """
        Converte grafo do tipo 'metabolite-reaction' para 'reaction-reaction'
        
        Parameters
        ----------
        :param gmr: Grafo a converter
        """
        for r in gmr.node_types["reaction"]:
            self.add_vertex(r)
            sucs = gmr.get_successors(r)
            for s in sucs:
                sucs_r = gmr.get_successors(s)
                for s2 in sucs_r:
                    if r != s2: self.add_edge(r, s2)

    
    def all_degrees (self, deg_type:str = "inout") -> dict:
        """
        Devolve um dicionário com os graus desejados
        
        Parameters
        ----------
        :param deg_type: Define o tipo de graus a serem calculados ('in', 'out' ou 'inout')
        """
        deg_type = deg_type.lower()
        assert deg_type in ["in","out","inout"], "Parâmetro 'deg_type' deve ser 'in','out','inout'" 
        
        degs = {}
        for v in self.graph.keys():
            if deg_type == "out" or deg_type == "inout":
                degs[v] = len(self.graph[v])
            else: degs[v] = 0
        if deg_type == "in" or deg_type == "inout":
            for v in self.graph.keys():
                for d in self.graph[v]:
                    if deg_type == "in" or v not in self.graph[d]: #Se for "inout", não pode acrescentar repetidos
                        degs[d] += 1
        return degs


    def mean_degree (self, deg_type:str = "inout") -> float:
        """
        Devolve o grau médio que se deseja calcular
        
        Parameters
        ----------
        :param deg_type: Define o tipo de graus a serem calculados ('in', 'out' ou 'inout')
        """
        degs = self.all_degrees(deg_type)
        return round(sum(degs.values()) / float(len(degs)), 4)
    
    
    def prob_degree (self, deg_type:str = "inout") -> dict:
        """
        Devolve um dicionário com a probabilidade de cada valor de grau ser encontrado no grafo
        
        Parameters
        ----------
        :param deg_type: Define o tipo de graus a serem calculados ('in', 'out' ou 'inout')
        """
        degs = self.all_degrees(deg_type)
        res = {}
        for k in degs.keys():
            if degs[k] in res.keys(): #Calculates number of times a degree value appears in the graph
                res[degs[k]] += 1
            else:
                res[degs[k]] = 1
        for k in res.keys():
            res[k] = round(res[k] / float(len(degs)), 4)
        return res
    
    
    def mean_distances(self) -> tuple:
        """
        Devolve um tuplo contendo média das distâncias entre cada par de nodos
        e a proporção de nós atingíveis
        """
        tot = 0
        num_reachable = 0
        for k in self.graph.keys():
            distsk = self.reachable_with_dist(k)
            for _, dist in distsk:
                tot += dist
            num_reachable += len(distsk)
        meandist = float(tot) / num_reachable
        return round(meandist, 4)
    
    
    def clustering_coef(self, v:str) -> float:
        """
        Devolve o coeficiente de clustering de um nodo do grafo
        """
        if v not in self.graph:
            return 0
        else:
            adjs = self.get_adjacents(v)
            if len(adjs) <= 1:
                return 0.0
            ligs = 0
            for i in adjs:
                for j in adjs:
                    if i != j:
                        if j in self.graph[i] or i in self.graph[j]: #Assim não há repetição??
                            ligs += 1
            return float(ligs)/(len(adjs)*(len(adjs)-1))


    def all_clustering_coefs(self) -> dict:
        """
        Devolve o coeficiente de clustering de cada nodo do grafo
        """
        ccs = {}
        for k in self.graph.keys():
            ccs[k] = self.clustering_coef(k)
        return ccs
    
    
    def mean_clustering_coef(self) -> float:
        """
        Devolve a média dos coeficiente de clustering de cada nodo do grafo
        """
        ccs = self.all_clustering_coefs()
        return sum(ccs.values()) / float(len(ccs))


    def mean_clustering_perdegree (self, deg_type:str = "inout"):
        """
        Devolve a média dos coeficientes de clustering de cada nodo associado a cada grau
        
        Parameters
        ----------
        :param deg_type: Define o tipo de graus a serem calculados ('in', 'out' ou 'inout')
        """
        degs = self.all_degrees(deg_type)
        ccs = self.all_clustering_coefs()
        degs_k = {} #grau: [nodos com o respetivo grau]
        for k in degs.keys():
            degs_k[degs[k]] = degs_k.get(degs[k],[]) + [k]
        ck = {} #grau: média do coef clustering dos respetivos nodos
        for k in degs_k.keys():
            tot = 0
            for v in degs_k[k]: tot += ccs[v]
            ck[k] = round(float(tot) / len(degs_k[k]), 4)
        return ck
    
    
    
    def reacoes_ativas(self, all_subs:list):
        """
        Devolve uma lista de reações ativas dada uma lista de substratos
        
        Parameters
        ----------
        :param all_subs: Lista de substratos
        """
        if self.net_type != "metabolite-reaction":
            return []

        active = []
        for r in self.node_types["reaction"]:
            pred = self.get_predecessors(r)
            if all([p in all_subs for p in pred]):
                active.append(r)
        return active
    
    
    def metabolitos_produzidos(self, active_r:list):
        """
        Devolve uma lista de metabolitos que podem ser produzidos dado
        uma lista de reações ativas
        
        Parameters
        ----------
        :param active_r: Lista de reações ativas
        """
        if self.net_type != "metabolite-reaction":
            return []
        
        result = []
        for act in active_r:
            result.extend(self.graph[act])
        return list(set(result)) #Eliminar repetidos
    
    
    def metabolitos_finais(self, met_iniciais:list):
        """
        Devolve uma lista de todos os metabolitos que podem ser produzidos
        a partir de uma lista de metabolitos iniciais
        
        Parameters
        ----------
        :param met_iniciais: Lista de metabolitos iniciais
        """
        if len(met_iniciais) == 0 or self.net_type != "metabolite-reaction":
            return []
        
        final = []
        while True:
            active_r = self.reacoes_ativas(met_iniciais)
            met_prod = self.metabolitos_produzidos(active_r)
            if (len(met_prod) != 0) and (not all([m in final for m in met_prod])):
                for met in met_prod:
                    if met not in final:
                        final.append(met)
                        met_iniciais = list(set(met_iniciais + final)) #Juntar novos metabolitos aos iniciais
            else:
                break
        return final

 