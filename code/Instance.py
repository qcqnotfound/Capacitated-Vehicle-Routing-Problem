from Node import Node

import numpy as np 
import math

class Instance:
    def __init__(self, path):
        # Open file
        file = open(path, "r").read().splitlines()
        
        # Name of the instance
        self.__name = file[0].split()[2]
        # Number of tracks / routes
        self.__k = int(self.__name[7:])
        # Number of nodes
        self.__dimension = int(file[3].split()[2])
        # Capacity
        self.__capacity = int(file[5].split()[2])

        # List of nodes
        self.__nodes = []
        # Matrix of distances
        self.__distance_matrix = np.zeros((self.__dimension, self.__dimension))

        # Starting point for reading coords
        start = 7
        # Progressive id
        label = 0

        for i in range(start, (self.__dimension + start)):
            line = file[i].split()
            # Coord x
            x = int(line[1])
            # Coord y
            y = int(line[2])
            # Request 
            request = int(file[i + self.__dimension + 1].split()[1])
            # Node creation
            node = Node(label, x, y, request)
            # Add the node to list
            self.__nodes.append(node)
            label += 1

        # Calculate distance matrix
        self.__calculate_distances()

    def __calculate_distances(self):
        # Calculate distance between each couple of nodes
        for i in range(self.__dimension):
            for j in range(self.__dimension):
                self.__distance_matrix[i][j] = self.__euclidean_distance(self.__nodes[i], self.__nodes[j])

    def __euclidean_distance(self, node_a, node_b):
        dx = node_a.get_x() - node_b.get_x()
        dy = node_a.get_y() - node_b.get_y()

        return round(math.sqrt(math.pow(dx, 2) + math.pow(dy, 2)))

    def get_name(self):
        return self.__name
    
    def get_capacity(self):
        return self.__capacity

    def get_dimension(self):
        return self.__dimension

    def get_k(self):
        return self.__k
        
    def get_nodes(self):
        return self.__nodes

    def get_distance_matrix(self):
        return self.__distance_matrix
