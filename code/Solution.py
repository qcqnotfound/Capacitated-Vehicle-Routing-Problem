import random 
import math

class Solution:
    def __init__(self, instance, max_age):
        # Instance of the problem
        self.__instance = instance
        # Solution
        self.__solution = []
        # Fitness of the solution
        self.__fitness = 0
        # Max age solution could have
        self.__max_age = max_age
        # Is the solution feasible?
        self.__feasible = False

        # Set age of solution randomly
        self.__age = random.randint(0, int((2/3) * self.__max_age))

        # Initialize the solution
        self.__initialize_solution()
        # Compute fitness
        self.__compute_fitness()
    
    def __initialize_solution(self):
        # Number of clients
        n = self.__instance.get_dimension()
        # Number of vehicles
        k = self.__instance.get_k()
        # Capacity of each vehicle
        c = self.__instance.get_capacity()
        # Nodes of the instance without depot (node 0)
        nodes = self.__instance.get_nodes()[1:]
        # Distance matrix of the instance
        distance_matrix = self.__instance.get_distance_matrix()

        # Add k+1 depots (one at the beginning and one at the end)
        # Each route is represented by the nodes between two zeros
        self.__solution = [0 for i in range(k+1)]

        while(len(nodes) > 0):
            # Choose a random node from nodes
            random.shuffle(nodes)
            node = nodes.pop().get_label()
            # Put the node in the route that minimize the cost
            dist = math.inf
            pos = 0
            for i in range(1, len(self.__solution)):
                if self.__solution[i] == 0:
                    new_dist = distance_matrix[self.__solution[i-1], node]
                    if new_dist < dist:
                        dist = new_dist
                        pos = i
            self.__solution.insert(pos, node)

    def __compute_fitness(self):
        # Compute cost 
        distance_matrix = self.__instance.get_distance_matrix()
        cost = 0
        for i in range(1, len(self.__solution)):
            last_node = self.__solution[i-1]
            current_node = self.__solution[i]
            cost += distance_matrix[last_node, current_node]

        # Compute the violation of the capacity 
        nodes = self.__instance.get_nodes()
        capacity = self.__instance.get_capacity()
        violation = 0
        cap = 0
        for i in range(len(self.__solution)):
            c = self.__solution[i]
            # On Depot
            if c == 0:
                if cap > capacity:
                    violation += (cap - capacity)
                cap = 0
            # On Client
            else:
                cap += nodes[c].get_request()

        if violation > 0:
            self.__feasible = False
        else:
            self.__feasible = True

        # Compute final fitness
        self.__fitness = cost + (100 * violation)

    def __swap(self, array, a, b):
        tmp = array[a]
        array[a] = array[b]
        array[b] = tmp

    def __move(self):
        point = random.randint(1, len(self.__solution)-2)
        position = random.randint(1, len(self.__solution)-2)
        node = self.__solution.pop(point)
        self.__solution.insert(position, node)

    def __reverse(self):
        a = random.randint(1, len(self.__solution)-2)
        b = random.randint(1, len(self.__solution)-2)

        if a > b:
            while(a > b):
                self.__swap(self.__solution, a, b)
                a -= 1
                b += 1
        if a < b:
            while(a < b):
                self.__swap(self.__solution, a, b)
                a += 1
                b -= 1

    def __two_opt(self, route):
        def calculate_cost(route):
            # Compute cost 
            distance_matrix = self.__instance.get_distance_matrix()
            cost = distance_matrix[0, route[0]]
            for i in range(1, len(route)):
                last_node = route[i-1]
                current_node = route[i]
                cost += distance_matrix[last_node, current_node]
            return cost + distance_matrix[route[-1], 0]
        
        # Length of the route
        route_len = len(route)
        # Current best cost
        best_distance = calculate_cost(route)
        # Best route found so far
        best_route = route
        
        for i in range(route_len):
            for j in range(i+1, route_len):
                # Swap elements with 2-OPT swap
                new_route = []
                for k in range(0, i):
                    new_route.append(route[k])
                for k in range(j, i-1, -1):
                    new_route.append(route[k])
                for k in range(j+1, route_len):
                    new_route.append(route[k])
                
                # Calculate new cost
                new_distance = calculate_cost(new_route)
                # Update
                if new_distance < best_distance:
                    best_route = new_route
                    best_distance = new_distance

        return best_route

    def hypermutation(self, rho, best, worst):
        # Improve the best fitness
        best = best / 2
        # Normalize fitness between 0 to 1
        norm_fitness = (worst - self.__fitness) / (worst - best)
        # Mutation rate
        alpha = math.exp(-rho * norm_fitness)
        # Number of mutation
        number_of_mutation = math.floor(1 + (alpha * self.__instance.get_dimension()))
        
        for i in range(number_of_mutation):
            r = random.random()
            if r < 0.5:
                self.__move()
            else:
                self.__reverse()

        self.__compute_fitness()

    def local_search(self):
        new_solution = [0]
        current_route = []
        for i in range(1, len(self.__solution)):
            if self.__solution[i] == 0:
                current_route = self.__two_opt(current_route)
                new_solution += current_route + [0]
                current_route.clear()
            else:
                current_route.append(self.__solution[i])
        self.__solution = new_solution
        self.__compute_fitness()

    def increment_age(self):
        self.__age += 1

    def set_random_age(self):
        self.__age = random.randint(0, int((2/3) * self.__max_age))

    def get_solution(self):
        return self.__solution

    def get_fitness(self):
        return self.__fitness

    def get_status(self):
        return self.__feasible

    def get_age(self):
        return self.__age