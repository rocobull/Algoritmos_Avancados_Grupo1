# -*- coding: utf-8 -*-

import random
class Entity:

	"""
	Gera um indivíduo.
	"""

	def __init__(self, size: int, genes: list, lb: int, ub: int) -> None:
		"""
		Inicializa uma instância da classe Entity.

		Parameters
		----------
		:param size: A dimensão do indivíduo
		:param genes: Os "genes" do indivíduo
		:param lb: O limite inferior dos números reais que representam os "genes" do indivíduo
		:param ub: O limite superior dos números reais que representam os "genes" do indivíduo
		"""

		self.size = size
		self.genes = genes
		self.lb, self.ub = lb, ub
		self.fitness = 0
		self.positions = []
		if not self.genes:
			self.genes = [random.uniform(lb, ub) for i in range(size*4)]


class Evolutionary:

	"""
	Implementa um algoritmo evolucionário para a procura de motifs num conjunto de sequências de DNA.
	"""
	

	def __init__(self, num_indivs: int, size_indiv: int, num_iter: int, alignment: str) -> None:
		"""
		Inicializa uma instância da classe Evolutionary.

		Parameters
		----------
		:param num_indivs: Número de indivíduos na população
		:param size_indiv: Dimensão de cada um dos indivíduos da população
		:param num_iter: Número de iterações a efetuar pelo algoritmo evolucionário
		:param alignment: O alinhamento de sequências no qual se pretende procurar motifs
		"""
		if type(num_indivs) != int:
			raise TypeError("O num_indivs deve ser do tipo inteiro")
		
		if type(size_indiv) != int:
			raise TypeError("O size_indiv deve ser do tipo inteiro")
		
		if type(num_iter) != int:
			raise TypeError("O num_iter deve ser do tipo inteiro")
		
		if type(alignment) != str:
			raise TypeError("O alignment deve ser do tipo string")

		self.num_indivs = num_indivs
		self.size_indiv = size_indiv
		self.population = [Entity(size_indiv, [], 0, 1) for i in range(num_indivs)]
		self.num_iter = num_iter
		self.alignment = [line.strip().upper() for line in open(alignment).readlines() if line.strip()]


	########## AVALIAR OS INDIVÍDUOS DA POPULAÇÃO ##########

	def __get_pwm(self, indiv: list) -> list:
		"""
		Retorna um perfil probablístico PWM construído a partir dos "genes" de um indivíduo.

		Parameters
		----------
		:param indiv: O indivíduo para o qual se pretende construír o PWM
		"""
		genes = indiv.genes
		# colocar "genes" no pwm
		pwm = []
		for i in range(len(genes)):
			if i % 4 == 0: 
				pwm += [{n: genes[i+j] for j,n in enumerate("ATCG")}]
		# normalizar as colunas do pwm
		for col in pwm:
			total = sum(col.values())
			for k in col:
				col[k] /= total
		return pwm

	def __get_best_seq(self, pwm: list) -> str:
		"""
		Retorna a sequência com maior probabilidade de ter sido gerada pelo PWM que toma como parâmetro.

		Parameters
		----------
		:param pwm: O perfil probablístico PWM 
		"""
		best_seq = ""
		for col in pwm:
			sorted_values = sorted(col.items(), key = lambda x: x[1])
			best_seq += sorted_values[0][0]
		return best_seq

	def __get_indiv_attr(self, seq: str) -> tuple:
		"""
		Retorna os valores de fitness de cada indivíduo e as posições no alinhamento de sequências que melhor se 
		adequam ao mesmo.

		Parameters
		----------
		:param seq: A sequência de DNA (motif) associada cada indivíduo.
		"""
		max_score, positions = 0, []
		for sequence in self.alignment:
			score, pos = 0, 0
			for i in range(len(sequence)-len(seq)+1):
				scr = 0
				for j in range(len(seq)):
					if sequence[i+j] == seq[j]: scr += 2
					else: scr -= 1
				if scr > score:
					score, pos = scr, i
			max_score += score
			positions += [pos]
		return max_score, positions

	def __evaluate(self) -> None:
		"""
		Avalia todos os indivíduos da população num determinado momento, atribuindo-lhes um valor de fitness, e
		uma lista de posições no alinhamento de sequências associadas ao mesmo.
		"""
		for indiv in self.population:
			pwm = self.__get_pwm(indiv)
			best_seq = self.__get_best_seq(pwm)
			indiv.fitness, indiv.positions = self.__get_indiv_attr(best_seq)
			print(f"Score: {indiv.fitness} | Positions: {indiv.positions}") # retirar: apenas para visualização
		print("") # retirar


	########## PROVOCAR MUTAÇÕES, RECOMBINAR INDIVÍDUOS, E GERAR NOVA POPULAÇÃO ##########

	def __get_best_indivs(self) -> list:
		"""
		Retorna os indivíduos melhor adaptados na população (50%).
		"""
		indivs = self.population
		sorted_indivs = sorted(indivs, key = lambda x: x.fitness)
		return sorted_indivs[self.num_indivs//2:]

	def __mutation(self, indivs: list) -> None:
		"""
		Provoca uma mutação num dos "genes" de cada indivíduo presente na lista que toma como parâmetro.

		Parameters
		----------
		:param indiv: Os indivíduos da população que sofrem mutação
		"""
		for indiv in indivs:
			ind = random.randint(0, self.size_indiv*4-1)
			new = random.uniform(indiv.lb, indiv.ub)
			indiv.genes[ind] = new

	def __get_progeny(self, indivs: list) -> list:
		"""
		Retorna a descendência de um dado conjunto de indivíduos.

		Parameters
		----------
		:param indivs: Os indivíduos cuja descendência se pretende determinar
		"""
		progeny = [Entity(indiv.size, indiv.genes[:], indiv.lb, indiv.ub) for indiv in indivs]
		idx = random.randint(self.size_indiv, self.size_indiv*3) # gets crossover site
		for i in range(0, len(progeny)-1, 2):
			temp = progeny[i].genes[:idx]
			progeny[i].genes[:idx] = progeny[i+1].genes[:idx]
			progeny[i+1].genes[:idx] = temp 
		self.__mutation(progeny)
		return progeny

	def __new_population(self) -> None:
		"""
		Constrói uma nova população tendo por base a população anterior, sendo constituída pelos indivíduos melhor
		adaptados na população anterior (metade da população) e pela sua descendência.
		"""
		best_indivs = self.__get_best_indivs()
		progeny = self.__get_progeny(best_indivs)
		self.population = best_indivs + progeny


	########## CORRER ALGORITMO EVOLUCIONÁRIO, E EXTRAÍR MOTIFS DAS SEQUÊNCIAS ##########

	def __run_ea(self) -> None:
		"""
		Corre o algoritmo evolucionário.
		"""
		for i in range(self.num_iter):
			self.__evaluate()
			self.__new_population()

	def get_motifs(self) -> list:
		"""
		Retorna uma lista de motifs presentes no alinhamento de sequências.
		"""
		self.__run_ea()
		sorted_indivs = sorted(self.population, key = lambda x: x.fitness)
		positions = sorted_indivs[-1].positions
		motifs = [self.alignment[i][pos:pos+self.size_indiv] for i, pos in enumerate(positions)]
		return motifs

if __name__ == "__main__":
	evol = Evolutionary(num_indivs = 12, size_indiv = 6, num_iter = 20, alignment = "seqs.txt")
	print(f"motifs: {evol.get_motifs()}")
