from Solution import Solution

from copy import deepcopy

class Population:
    def __init__(self, instance, size, dup, max_age):
        # Instance of the problem
        self.__instance = instance
        # Size of population
        self.__size = size
        # Cloning parameter
        self.__dup = dup
        # Max age
        self.__max_age = max_age

        # Solutions of population
        self.__solutions = []
        # Cloned solutions
        self.__cloned_solutions = []

        for i in range(self.__size):
            self.__solutions.append(Solution(instance, max_age))

        self.__best = min(self.__solutions, key = lambda s : s.get_fitness())
        self.__worst = max(self.__solutions, key = lambda s : s.get_fitness())

    def increment_age(self):
        for i in range(self.__size):
            self.__solutions[i].increment_age()

    def clone(self):
        for i in range(self.__dup):
            # Do this dup times
            for j in range(self.__size):
                # Clone the solution
                clone = deepcopy(self.__solutions[j])
                # Set random age
                clone.set_random_age()
                # Push the solution to cloned_population
                self.__cloned_solutions.append(clone)

    def hypermutation(self, rho):
        for i in range(len(self.__cloned_solutions)):
            self.__cloned_solutions[i].hypermutation(rho, self.__best.get_fitness(), self.__worst.get_fitness())

    def local_search(self):
        for i in range(len(self.__solutions)):
            if self.__solutions[i].get_status() == True:
                self.__solutions[i].local_search() 

        # Update best and worst solutions
        self.__best = min(self.__solutions, key = lambda s : s.get_fitness())
        self.__worst = max(self.__solutions, key = lambda s : s.get_fitness())

    def aging(self):
        # Join lists
        self.__solutions += self.__cloned_solutions
        # Clean cloned solutions
        self.__cloned_solutions.clear()

        # Update best
        self.__best = min(self.__solutions, key = lambda s : s.get_fitness())

        # Find and save the best solution
        b_index = self.__solutions.index(self.__best)
        self.__solutions.pop(b_index)

        # Remove "dead" solutions and keep the best
        self.__solutions = [s for s in self.__solutions if s.get_age() <= self.__max_age]
        self.__solutions.append(self.__best)

    def select(self, best_per, worst_per):
        current_size = len(self.__solutions)
        if current_size < self.__size:
            for i in range(current_size, self.__size):
                s = Solution(self.__instance, self.__max_age)
                self.__solutions.append(s)
        else:
            self.__solutions.sort(key = lambda s : s.get_fitness())
            self.__solutions = self.__solutions[:best_per] + self.__solutions[-worst_per:]
            #self.__solutions = self.__solutions[:self.__size]

        # Update best and worst solutions
        #self.__best = min(self.__solutions, key = lambda s : s.get_fitness())
        #self.__worst = max(self.__solutions, key = lambda s : s.get_fitness())

    def get_solutions(self):
        return self.__solutions

    def get_best(self):
        return self.__best
        
    def get_worst(self):
        return self.__worst