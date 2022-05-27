# -*- coding: utf-8 -*-

"""
Class: BurrowsWheeler
"""

class BurrowsWheeler:

	"""
	Implementa a tranformação de Burrows-Wheeler para a compressão de sequências e procura de padrões.
	"""

	def __init__(self, seq: str):
		"""
		Inicializa uma instância da classe guardando a sequêcia introduzida, executa a transformação de Burrows-Wheeler, 
		chama o método __index_columns() para indexação da primeira e última colunas, e constrói um dicionário de caminhos 
		que associa a última coluna indexada à primeira coluna indexada da transformada.

		Parameters
		----------
		:param seq: A sequência de caracteres introduzida pelo utilizador
		"""

		if type(seq) is not str:
			raise TypeError("O parâmetro 'seq' deve ser do tipo 'str'.")

		seq += "$"
		self.bwt = sorted([(seq[i:].upper() + seq[:i].upper(), i) for i in range(len(seq))])
		self.first_ind, self.last_ind = self.__index_columns()
		self.offsets = [row[1] for row in self.bwt]
		self.path_dic = {k: v for k, v in zip(self.last_ind, self.first_ind)}
		
	def __str__(self) -> str:
		"""
		Imprime a matriz de rotações (self.bwt) gerada pela tranformação de Burrows-Wheeler de uma forma percetível.
		"""
		out = "\nMatriz de rotações\n"
		for row in self.bwt:
			out += " ".join(row[0]) + "\n"
		return out

	def _index_chars(self, col: list) -> list:
		"""
		Recebe uma coluna da matriz de rotações e indexa todos os caracteres dessa coluna.

		Parameters
		----------
		:param col: A coluna da matriz de rotações de Burrows-Wheeler a indexar 
		"""
		dic = {k: 0 for k in set(col)}
		for i,c in enumerate(col):
			col[i] = c + str(dic[c])
			dic[c] += 1
		return col

	def __index_columns(self) -> tuple:
		"""
		Indexa a primeira e última colunas da matriz de rotações.
		"""
		first_col = [row[0][0] for row in self.bwt]
		last_col = [row[0][-1] for row in self.bwt]
		return self._index_chars(first_col), self._index_chars(last_col)

	def compress(self) -> str:
		"""
		Comprime a transformada de Burrows-Wheeler. Caso a versão comprimida tenha uma dimensão inferior à versão original,
		retorna a versão comprimida. Caso contrário, retorna a versão original.
		"""
		last_col = "".join([row[0][-1] for row in self.bwt])
		compressed = ""
		i = 0
		while i < len(last_col):
			num_reps = 1
			for j in range(i, len(last_col)):
				if j+1 < len(last_col):
					if last_col[j] == last_col[j+1]: num_reps += 1
					else: break
			compressed += f"{str(num_reps)}{last_col[i]}"
			i += num_reps
		if len(compressed) < len(last_col): out = compressed
		else: out = last_col 
		return out

	def rebuild_seq(self) -> str:
		"""
		Reconstrói a sequência original com o auxílio de um dicionário de caminhos (self.path) criado a partir da primeira e
		última colunas indexadas da matriz de rotações de Burrows-Wheeler.
		"""
		seq_res = ""
		x = "$0"
		while self.path_dic[x] != "$0":
			seq_res += self.path_dic[x][0]
			x = self.path_dic[x]
		return seq_res

	def search_pattern(self, sub: str) -> list:
		"""
		Recebe um padrão e constrói um array de caminhos à medida que os caracteres do mesmo são iterados. Retorna as posições
		em que o padrão é encontrado na sequência.

		Parameters
		----------
		:param sub: O padrão a procurar na sequência
		"""

		if type(sub) is not str:
			raise TypeError("O parâmetro 'sub' deve ser do tipo 'str'.")

		paths = [[v for k, v in self.path_dic.items() if v[0] == sub[0]]]
		ct = 1
		while ct < len(sub):
			paths += [[self.path_dic[c] for c in paths[ct - 1] if self.path_dic[c][0] == sub[ct]]]
			ct += 1
		pos = [(self.offsets[self.first_ind.index(c)] - (len(sub)-1)) for c in paths[-1]]
		return sorted(pos)
