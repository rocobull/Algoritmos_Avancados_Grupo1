# -*- coding: utf-8 -*-

from typing import Union

class DeBruijn:

	"""
	Implementa o algoritmo de DeBruijn para a reconstrução de sequências de DNA.
	"""

	def __init__(self, kmers: list) -> None:
		"""
		Inicializa uma instância da classe DeBruijn, guardando os k-mers introduzidos pelo utilizador.

		Parameters
		----------
		:param kmers: Os k-mers introduzidos pelo utilizador
		"""

		if type(kmers) is not list and type(kmers) is not tuple:
			raise TypeError("O parâmetro 'kmers' deve ser do tipo 'list' ou 'tuple'.")

		for kmer in kmers:
			if type(kmer) is not str:
				raise TypeError("Cada um dos k-mers deve ser do tipo 'str'.")

		self.kmers = sorted([kmer.upper() for kmer in kmers])
		self.de_bruijn = self.get_de_bruijn()

	def __str__(self) -> str:
		"""
		Imprime os k-mers introduzidos pelo utilizador.
		"""
		return f"Fragmentos: {str(self.kmers)}"


	########## CONSTRUÇÃO DO GRAFO ##########

	def get_nodes(self) -> list:
		"""
		A partir dos k-mers, retorna uma lista de nodos que irão compor o grafo. 
		"""
		len_kmers = len(self.kmers[0])
		return [(k[:len_kmers-1], k[1:]) for k in self.kmers]

	def get_de_bruijn(self) -> dict:
		"""
		Retorna o grafo que auxilia na execução do algoritmo de DeBruijn. Consiste num dicionário de dicionários 
		em que os values dos dicionários interiores correspondem ao número de arcos existentes entre os nodos 
		que o compõem.

		de_bruijn = {"aa": {"ab": 1, "ac": 2},
					 "bb": {"ba": 3, "bc": 2}}
					 "cc": {"ca": 2, "cb": 1}}} 

		"""
		nodes = self.get_nodes()
		de_bruijn = {}
		for tup in nodes:
			fr, to = tup
			if fr not in de_bruijn: de_bruijn[fr] = {to: 1} 
			else:
				if to in de_bruijn[fr]: de_bruijn[fr][to] += 1
				else: de_bruijn[fr][to] = 1
		# verificar se todos os nodos são keys do grafo
		nodes_list = [node for tup in nodes for node in tup]
		for node in nodes_list:
			if node not in de_bruijn: de_bruijn[node] = {"?": 0}
		return de_bruijn


	########## VALIDAÇÃO, EMPARELHAMENTO DE NODOS NÃO BALANCEADOS, E DETERMINAÇÃO DE ORIGENS ##########

	def get_out_degree(self, node: str) -> int:
		"""
		Retorna o grau de saída do nodo que toma como parâmetro.

		Parameters
		----------
		:param node: O nodo cujo grau de saída se pretende determinar
		"""
		out_deg = 0
		for k in self.de_bruijn[node]:
			out_deg += self.de_bruijn[node][k]
		return out_deg

	def get_in_degree(self, node: str) -> int:
		"""
		Retorna o grau de entrada do nodo que toma como parâmetro.

		Parameters
		----------
		:param node: O nodo cujo grau de entrada se pretende determinar
		"""
		in_deg = 0
		for k in self.de_bruijn:
			if node in self.de_bruijn[k]: in_deg += self.de_bruijn[k][node]
		return in_deg

	def validate_eulerian(self) -> bool:
		"""
		Verifica se um grafo é ou não Euleriano.
		"""
		begin = end = 0 
		res = True
		for node in self.de_bruijn:
			out_deg, in_deg = self.get_out_degree(node), self.get_in_degree(node)
			# verificar condição |out_degree - in_degree| > 1
			if abs(out_deg - in_deg) > 1:
				res = False
				break
			# verificar número de nodos com out_deg > in_deg e com in_deg > out_deg
			if out_deg > in_deg: begin += 1
			elif out_deg < in_deg: end += 1
		# verificar condição "nº de nodos com (out_deg-in_deg==1) == nº de nodos com (out_deg-in_deg==-1)"
		if begin != end: res = False
		return res

	def get_unbalanced(self) -> Union[list, bool]:
		"""
		Caso o grafo seja Euleriano, retorna uma lista com as origens dos contigs. Caso contrário, retorna False.
		"""
		valid = self.validate_eulerian()
		if valid:
			starts, ends = [], []
			for node in self.de_bruijn:
				out_deg, in_deg = self.get_out_degree(node), self.get_in_degree(node)
				if out_deg - in_deg == 1: starts += [node]
				if in_deg - out_deg == 1: ends += [node]
			if not starts: starts += [list(self.de_bruijn.keys())[0]] # caso todos os nodos sejam balanceados
		else: return valid
		return starts, ends

	def pair_unbalanced(self, starts: list, ends: list) -> None:
		"""
		Emparelha os nodos não balanceados do grafo.

		Parameters
		----------
		:param starts: Uma lista de nodos que apresentam um maior grau de saída que de entrada
		:param ends: Uma lista de nodos que apresentam um maior grau de entrada que de saída
		"""
		for end, start in zip(ends, starts):
			if list(self.de_bruijn[end].keys())[0] == "?":
				self.de_bruijn[end] = {start: 1}
			else:
				if start in self.de_bruijn[end]: self.de_bruijn[end][start] += 1
				else: self.de_bruijn[end][start] = 1


	########## RECONSTRUÇÃO DA(S) SEQUÊNCIA(S) ##########

	def get_loop(self, curr: str) -> list:
		"""
		Retorna uma lista de nodos que formam uma laçada no grafo.

		Parameters
		----------
		:param curr: O nodo de origem da laçada
		"""
		nodes = []
		while curr in self.dbr_copy:
			nxt = list(self.dbr_copy[curr].keys())[0]
			nodes += [nxt]
			self.dbr_copy[curr][nxt] -= 1
			if self.dbr_copy[curr][nxt] == 0: del self.dbr_copy[curr][nxt]
			if not self.dbr_copy[curr]: del self.dbr_copy[curr]
			curr = nxt
		return nodes

	def flat_list(self, node_list: list) -> list:
		"""
		Tranforma a lista que toma como parâmetro numa lista unidimensional.

		Parameters
		----------
		:param node_list: A lista a ser transformada
		"""
		out = []
		for item in node_list:
			if type(item) is list: out += item
			else: out += [item]
		return out

	def rebuild_seqs(self) -> Union[list, str]:
		"""
		Caso o grafo seja Euleriano, retorna uma lista contendo todos os contigs reconstruídos. Caso contrário, 
		retorna uma mensagem de erro.  
		"""
		unbalanced = self.get_unbalanced()
		if unbalanced:
			starts, ends = unbalanced
			self.pair_unbalanced(starts, ends)
			self.dbr_copy = {k1: {k2: v for k2, v in self.de_bruijn[k1].items()} for k1 in self.de_bruijn} # cópia
			contigs = []
			while starts:
				nodes = [starts.pop(0)]
				while self.dbr_copy:
					found = False
					for i, node in enumerate(nodes):
						if node in list(self.dbr_copy.keys()):
							curr = node
							found = True
							break
					if not found: break
					loop = self.get_loop(curr)
					nodes.insert(i+1, loop)
					nodes = self.flat_list(nodes)
				contig = nodes[0]
				for node in nodes[1:]:
					contig += node[-1]
				if len(contig) > len(self.kmers) + 2: contigs += [contig[:-1]]
				else: contigs += [contig]
			out = contigs
		else:
			out = "ERRO: O grafo não é Euleriano!"
		return out
