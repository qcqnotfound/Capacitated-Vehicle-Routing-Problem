from Instance import Instance
from Solution import Solution
from Population import Population
import random

best_solutions = []

POPULATION_SIZE = 100
DUP = 2
MAX_AGE = 5
RHO = 10

RUNS = 5
MAX_EPOCH = 10000

# Instance of the problem
instance = Instance("Instances/A-n32-k5.vrp")

for run in range(RUNS):
    # Initial population
    population = Population(instance, POPULATION_SIZE, DUP, MAX_AGE)

    for e in range(MAX_EPOCH):
        # Epoch
        print("Epoch: ", e)

        # Increment age
        population.increment_age()

        # Cloning
        population.clone()

        # Hypermutation
        population.hypermutation(RHO)

        # Aging
        population.aging()

        # Selection
        population.select(int(POPULATION_SIZE * 0.6), int(POPULATION_SIZE * 0.4))

        # Local Search
        population.local_search()

        # Best and worst solution
        print("Best: ", population.get_best().get_fitness())
        #print("Worst: ", population.get_worst().get_fitness())

        if population.get_best().get_fitness() == 784:
            break

    best_solutions.append(population.get_best().get_fitness())

print("\n")

# Best solution
print("Best: ", min(best_solutions))

# Worst solution
print("Worst: ", max(best_solutions))

# Average
avg = sum(best_solutions)/len(best_solutions)
print("Average: ", avg)

# Standard deviation
term = 0
for s in best_solutions:
    term += (s - avg)**2
term = term / (len(best_solutions) - 1)
std = term**(1/2)
print("Standard deviation: ", std)
