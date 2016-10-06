from random import random, randrange

MAX_POP = 100
MAX_STRING = 30
P_CROSS = P_MUTATION = SUM_FITNESS = 0.0
N_MUTATION = N_CROSS = 0
AVG = MAX = MIN = 0.0


class Individual:
    def __init__(self, chrom, parent1, parent2, cross_point):
        self.chrom = chrom
        self.parent1 = parent1
        self.parent2 = parent2
        self.cross_point = cross_point

    @classmethod
    def new(cls, chrom_len):
        chrom = ''.join(['1' if random() < 0.5 else '0' for _ in range(chrom_len)])
        return cls(chrom, None, None, None)

    def __getattr__(self, item):
        if item == 'x':
            self.x = self.decode()
        elif item == 'fitness':
            self.fitness = self.objective_function()
        else:
            raise AttributeError("'{}' object has no attribute {}".format(type(self).__name__, item))

    def decode(self):
        return int(self.x, 2)

    def objective_function(self):
        coef = 2 ** 30 - 1
        n = 10

        return (self.x / coef) ** n

    def mutate(self, p_mutation):
        mutator = {'0': '1', '1': '0'}
        self.chrom = ''.join([mutator[c] if random() < p_mutation else c for c in self.chrom])

    @staticmethod
    def crossover(mate1, mate2, p_crossover, p_mutation):
        assert len(mate1.chrom) == len(mate2.chrom)

        chrom_len = len(mate1.chrom)

        if random() < p_crossover:
            cross_point = randrange(1, chrom_len)
            child1_chrom = mate1[:cross_point] + mate2[cross_point:]
            child2_chrom = mate2[:cross_point] + mate1[cross_point:]
            child1 = Individual(child1_chrom, mate1, mate2, cross_point)
            child2 = Individual(child2_chrom, mate2, mate1, cross_point)
        else:
            child1 = Individual(mate1.chrom, mate1, mate2, chrom_len)
            child2 = Individual(mate2.chrom, mate2, mate1, chrom_len)
        child1.mutate(p_mutation)
        child2.mutate(p_mutation)

        return child1, child2


class Population:
    def __init__(self, size, chrom_len, p_crossover, p_mutation):
        self.individuals = [Individual.new(chrom_len) for _ in range(size)]
        self.old_individuals = None
        self.size = size
        self.p_crossover = p_crossover
        self.p_mutation = p_mutation
        self.sum_fitness = sum([individual.fitness for individual in self.individuals])
        self.generation_num = 0

    def select(self):
        partial_sum = self.individuals[0]
        target = random() * self.sum_fitness
        individual = None

        for individual in self.individuals:
            if partial_sum >= target:
                break

        return individual

    def generation(self):
        new_individuals = []

        while len(new_individuals) < self.size:
            mate1 = self.select()
            mate2 = self.select()
            children = Individual.crossover(mate1, mate2, self.p_crossover, self.p_mutation)
            new_individuals.extend(children)

        self.old_individuals = self.individuals
        self.individuals = new_individuals
        self.sum_fitness = sum([individual.fitness for individual in self.individuals])
