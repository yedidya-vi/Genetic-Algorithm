import numpy as np
import math
import random
import statistics as st

class Genetic_Algorithm():

    def __init__(self, initial_population):
        self.population = initial_population
        self.num_of_queens = len(initial_population[0])
        self.num_of_individuals = len(initial_population)
        self.max_fitness = (n-1)*n/2

    def all_individual_pairs(self, individual):
        pairs = np.empty([0, 4])
        for j in range(self.num_of_queens):
            for i in range(j + 1, self.num_of_queens):
                pairs = np.insert(pairs,
                                  0,
                                  (individual[j], individual[i], j + 1, i + 1),
                                  axis=0)

        return pairs

    def all_states_pairs(self):
        all_states_pairs = np.empty([0,int(self.max_fitness),4])
        for individual in self.population:
            all_states_pairs = np.insert(all_states_pairs,
                                         len(all_states_pairs),
                                         Genetic_Algorithm.all_individual_pairs(self,
                                                                                individual),
                                         axis = 0)

        return all_states_pairs

    def state_values(self, all_states_pairs):
        state_values = []
        for state_pairs in all_states_pairs:
            state_values.append(Genetic_Algorithm.fitness_function(self, state_pairs))

        return state_values

    def fitness_function(self, all_pairs):
        value = self.max_fitness
        for pair in all_pairs:
            value -= Genetic_Algorithm.check_pair(self,
                                                  pair[0],
                                                  pair[1],
                                                  pair[2],
                                                  pair[3])

        return value

    def check_pair(self, queen_a, queen_b, index_a, index_b):
        if queen_a == queen_b:
            return 1
        elif abs(queen_b - queen_a) == abs(index_b - index_a):
            return 1
        else:
            return 0

    def random_selection(self):
        all_states_pairs = Genetic_Algorithm.all_states_pairs(self)
        state_values = Genetic_Algorithm.state_values(self, all_states_pairs)
        states_per = []
        for state_value in state_values:
            states_per.append((state_value - min(state_values)) ** 4)
        x = random.choices(self.population, weights=states_per, k=int(self.num_of_individuals/2))
        y = random.choices(self.population, weights=states_per, k=int(self.num_of_individuals/2))

        return x, y

    def Reproduce(self, parent_x, parent_y,n):
        children = []
        for i in range(self.num_of_individuals):
            c = np.random.randint(int(n/2)-1, int(n/2)+2)
            children.append(np.concatenate((parent_x[math.floor(i / 2)][0:c],
                                            parent_y[math.floor(i / 2)][c:self.num_of_queens])))

        return np.array(children)

    def Mutation(self, children):
        for child in children:
            rand = np.random.randint(5)
            if rand > 0:
                c = np.random.randint(0, self.num_of_queens)
                child[c] = np.random.randint(1, self.num_of_queens)

        return children

    def check_population(self, steps, beginnings):
        all_states_pairs = Genetic_Algorithm.all_states_pairs(self)
        state_values = Genetic_Algorithm.state_values(self, all_states_pairs)
        for i in range(len(state_values)):
            if state_values[i] == self.max_fitness:
                print('\nThe goal is:', self.population[i],
                      '\nThe goal was found after',150 - steps, 'generation and', int(1+beginnings/150), 'beginnings.')
                quit()

        return

#num of queens:
n = int(input("\nEnter number of queens: "))
#num of samples:
k = int(input("Enter number of samples in every ganeration: "))
#num of new generation
i = 0
#num of starters
beginnings = 0

while(True):
    if (i == 0):
        #Setting the initial generation
        generation = Genetic_Algorithm(np.random.randint(n, size=(k, n)) + 1)
        generation.check_population(i, beginnings)
        i = 150

    #Setting the next generation:
    parent_x, parent_y = generation.random_selection()
    children = generation.Reproduce(parent_x, parent_y, n)
    children_with_mutation = generation.Mutation(children)
    generation = Genetic_Algorithm(children_with_mutation)
    generation.check_population(i, beginnings)
    i -= 1
    beginnings +=1