# -*- coding: utf-8 -*-

import random
import re

"""
Class: PWM
"""

class PWM:

	"""
	Constrói um perfil pwm para cálculo da probabilidade de ocorrência de um dado motif
	"""

	def __init__(self, seqs: list, alphabet: str, pseudo: int) -> None:
		"""
		Inicializa uma instância da classe PWM, guardando uma lista de sequências, um alfabeto, uma pseudocontagem, e
		um perfil pwm gerado com o auxílio do método get_pwm()

		Parameters
		----------
		:param seqs: Uma lista de sequências
		:param alphabet: O alfabeto a utilizar
		:param pseudo: Um valor para a pseudocontagem
		"""
		self.seqs = seqs
		self.alphabet = alphabet
		self.pseudo = pseudo
		self.pwm = self.__get_pwm()

	def __str__(self) -> str:
		"""
		Imprime, de um modo legível, os parâmetros inseridos pelo utilizador aquando da criação de uma instância
		"""
		out = f"Sequences: {', '.join(self.seqs)}\nPseudocount: {self.pseudo}"
		return out

	def __get_pwm(self) -> list:
		"""
		Constrói um perfil pwm a partir da lista de sequências e da pseudocontagem fornecidas
		"""
		pwm = []
		total = len(self.seqs) + len(self.alphabet) * self.pseudo
		for sub in zip(*self.seqs):
			dic = {base: (sub.count(base) + self.pseudo) / total for base in self.alphabet}
			pwm.append(dic)
		return pwm

	def __subseq_prob(self, subseq: str) -> float:
		"""
		Determina a probabilidade de uma dada sequência ter sido gerada pelo perfil pwm

		Parameters
		----------
		:param subseq: A sequência cuja probabilidade de ocorrência é avaliada
		"""
		prob = 1.0
		for i in range(len(subseq)):
			prob *= self.pwm[i][subseq[i]]
		return prob

	def get_probs(self, seq: str) -> list:
		"""
		Chama o método subseq_prob() e avalia a probabilidade de todas as subsequências da sequência fornecida terem sido
		geradas pelo perfil pwm

		Parameters
		----------
		:param seq: A sequência a ser fragmentada e avaliada
		"""
		subseqs = re.findall(fr"(?=(.{{{len(self.pwm)}}}))", seq)
		return [self.__subseq_prob(subseq) for subseq in subseqs]

"""
Class: GibbsSampling
"""
	
class GibbsSampling:

	"""
	Implementa o método de Gibbs Sampling para a procura de motifs numa lista de sequências
	"""

	def __init__(self, seqs: list, alphabet: str, len_motif: int) -> None:
		"""
		Inicializa uma instância da classe GibbsSampling, guardando uma lista de sequências, um alfabeto, e o tamanho do 
		motif a procurar nas mesmas

		Parameters
		----------
		:param seqs: Lista de sequências introduzida pelo utilizador
		:param alphabet: O alfabeto a utilizar
		:param len_motif: Tamanho do motif a procurar nas sequências
		"""

		if type(seqs) is not list and type(seqs) is not tuple:
			raise TypeError("O parâmetro 'seqs' deve ser do tipo 'list' ou 'tuple'.")

		for seq in seqs:
			if type(seq) is not str:
				raise TypeError("Pelo menos uma das sequências inseridas não é do tipo 'str'")

		if type(alphabet) is not str:
			raise TypeError("O parâmetro 'alphabet' deve ser do tipo 'str'.")

		if type(len_motif) is not int:
			raise TypeError("O parâmetro 'len_motif' deve ser do tipo 'int'.")

		if len_motif <= 1 or len_motif >= len(seqs[0]):
			raise ValueError("O valor do parâmetro 'len_motif' deve estar no intervalo [2, len(sequences)-1].")

		self.seqs = [seq.upper() for seq in seqs]
		self.alphabet = alphabet
		self.len_motif = len_motif

	def __str__(self) -> str:
		"""
		Imprime, de um modo legível, os parâmetros inseridos pelo utilizador aquando da criação de uma instância
		"""
		out = f"Sequences: {', '.join(self.seqs)}\nAlphabet: {self.alphabet}\nMotif length: {self.len_motif}"
		return out

	def __get_indices(self) -> list:
		"""
		Gera uma lista de indíces (com a dimensão de self.seqs) de forma aleatória, cujos valores são determinados pelo 
		tamanho das sequências e do motif
		"""
		len_seqs = len(self.seqs[0])
		return [random.randint(0, len_seqs - self.len_motif) for i in range(len(self.seqs))]

	def __get_subseqs(self, inds: list, ind_out = None) -> list:
		"""
		Gera uma lista de subsequências, fragmentando as sequências originais nos índices especificados

		Parameters
		----------
		:param inds: Lista de índices utilizada na fragmentação das sequências
		:param ind_out: Índice da sequência que não é considerada (por omissão, None) 
		"""
		return [self.seqs[i][inds[i]:inds[i]+self.len_motif] for i in range(len(self.seqs)) if i != ind_out]

	def __get_seq_probs(self, indices: list, ind_out: int) -> list:
		"""
		Devolve uma lista contendo as probabilidades de cada subsequência de self.seqs[ind_out] ter sido gerada pelo
		perfil pwm construído a partir das restantes sequências de self.seqs

		Parameters
		----------
		:param indices: Lista de índices utilizada na geração de subsequências para a construção do perfil pwm
		:param ind_out: Índice da sequência cujas subsequências são sujeitas a análise probablística 
		"""
		subseqs = self.__get_subseqs(indices, ind_out) # subsequências com o tamanho do motif (não tendo em conta seq_out)
		pwm = PWM(subseqs, self.alphabet, 1) # construção do pwm (pseudocontagem == 1)
		return pwm.get_probs(self.seqs[ind_out])

	def __roullete_wheel(self, probs_list: list) -> int:
		"""
		Implementa uma roullete wheel para a determinação estocástica de um índice de uma lista

		Parameters
		----------
		:param probs_list: Lista de probabilidades que determina os pesos relativos para a seleção dos índices
		"""
		ind_list = [i for i in range(len(probs_list))]
		return random.choices(ind_list, weights = probs_list, k = 1)[0]

	def get_motifs(self, num_iter: int) -> list:
		"""
		Devolve uma lista de motifs, aplicando o método de Gibbs Sampling às sequências originais

		Parameters
		----------
		:param num_iter: Número máximo de iterações seguidas sem qualquer melhoria
		"""

		if type(num_iter) is not int:
			raise TypeError("O parâmetro 'num_iter' deve ser do tipo 'int'.")

		if num_iter <= 0:
			raise ValueError("O valor do parâmetro 'num_iter' deve estar no intervalo [1, inf].")

		indices = self.__get_indices() # índices iniciais obtidos aleatoriamente
		no_change = 0 # para a condição de término ***
		while no_change < num_iter: # ***
			ind_out = random.randint(0, len(self.seqs) - 1) # índice da sequência que ficará de fora (seq_out)
			seq_out_probs = self.__get_seq_probs(indices, ind_out) # probabilidades relativas às subsequências de seq_out
			ind_roullete = self.__roullete_wheel(seq_out_probs) # determinação do índice de forma estocástica
			if ind_roullete == indices[ind_out]: no_change += 1 # ***
			else: 
				no_change = 0 # ***
				indices[ind_out] = ind_roullete
		return self.__get_subseqs(indices)
