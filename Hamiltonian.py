# -*- coding: utf-8 -*-

from typing import Union

class Hamiltonian:

	"""
	Implementa um algoritmo para a reconstrução de sequências através de circuitos Hamiltonianos.
	"""

	def __init__(self, kmers: list) -> None:
		"""
		Inicializa uma instância da classe Hamiltonian, guardando uma lista de k-mers introduzida pelo utilizador e
		um grafo gerado com o auxílio do método self.get_graph().

		Parameters
		----------
		:param kmers: A lista de k-mers introduzida pelo utilizador
		"""

		if type(kmers) is not list and type(kmers) is not tuple:
			raise TypeError("O parâmetro 'kmers' deve ser do tipo 'list' ou 'tuple'.")

		for kmer in kmers:
			if type(kmer) is not str:
				raise TypeError("Cada um dos k-mers deve ser do tipo 'str'.")

		self.kmers = sorted([kmer.upper() for kmer in kmers])
		self.graph = self.get_graph()

	def __str__(self) -> str:
		"""
		Imprime os k-mers introduzidos pelo utilizador.
		"""
		return f"Fragmentos: {str(self.kmers)}"

	def get_graph(self) -> dict:
		"""
		Retorna um grafo na forma de dicionário em que os nodos são os k-mers introduzidos pelo utilizador. Os nodos são 
		numerados de modo a evitar repetições, e as ligações são formadas quando se verifica sobreposição entre o sufixo de 
		um k-mer e o prefixo do k-mer seguinte.
		"""
		graph = {}
		for i, x in enumerate(self.kmers):
			graph[f"{x}_{i}"] = []
			for j, y in enumerate(self.kmers):
				if i != j and x[1:] == y[:-1]:
					graph[f"{x}_{i}"] += [f"{y}_{j}"]
		return graph

	def validate_graph(self) -> bool:
		"""
		Verifica se o grafo contém todos os nodos e se não existem nodos repetidos.
		"""
		len_kmers = len(self.kmers[0])
		nodes = list(self.graph.keys())
		# verifica se todos os k-mers são nodos do grafo
		nodes_preffix = [node[:len_kmers] for node in nodes]
		if set(nodes_preffix) == set(self.kmers): res = True
		else: res = False
		# verifica se existe repetição de nodos no grafo
		if res:
			if len(set(nodes)) != len(nodes): res = False
		return res

	def hamiltonian_node(self, start: str) -> Union[None, list]:
		"""
		Considerando um determinado nodo como origem, verifica se existe um circuito Hamiltoniano no grafo.

		Parameters
		----------
		:param start: O nodo de origem
		"""
		current = start
		visited = {current: 0}
		path = [current]
		while len(path) < len(self.kmers):
			nxt_index = visited[current]
			if len(self.graph[current]) > nxt_index: # !***
				nxt_node = self.graph[current][nxt_index]
				visited[current] += 1
				if nxt_node not in path:
					path += [nxt_node]
					visited[nxt_node] = 0 # primeiro índice da lista de sucessores a procurar
					current = nxt_node
			else: # caso a lista seja vazia ou se tenham esgotado os índices da lista de sucessores ***
				if len(path) > 1:
					rmv_node = path.pop()
					del visited[rmv_node]
					current = path[-1] # :::
				else: return None # se len(path) == 1, ficamos sem nodos no path ::: 
		return path

	def hamiltonian(self) -> Union[None, list]:
		"""
		Verifica se existe pelo menos um nodo no grafo que permite a produção de um caminho Hamiltoniano quando considerado
		como origem. Caso exista, retorna um circuito Hamiltoniano que tem esse nodo como origem. Caso contrário, retorna None.
		"""
		for node in list(self.graph.keys()):
			path = self.hamiltonian_node(node)
			if path: return path
		return None

	def rebuild_seq(self) -> str:
		"""
		Reconstrói a sequência original a partir de um caminho Hamiltoniano. Caso o grafo não seja válido ou não exista qualquer 
		caminho Hamiltoniano no mesmo, retorna uma mensagem de erro.
		"""
		if self.validate_graph():
			path = self.hamiltonian()
			if path:
				len_kmers = len(self.kmers[0])
				out = path[0][:len_kmers]
				for node in path[1:]:
					out += node[len_kmers-1]
			else: out = "ERRO: Não existe qualquer circuito Hamiltoniano!"
		else: out = "ERRO: O grafo não contém todos os fragmentos, e/ou contém fragmentos repetidos!"
		return out
