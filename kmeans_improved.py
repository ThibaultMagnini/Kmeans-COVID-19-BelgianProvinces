import numpy as np
import pandas as pd
import random as rd
import matplotlib.pyplot as plt

# Class containing all the methods needed to perform kmeans clustering on a given dataset
class Kmeans:
    # Original dataset
    original_dataset = []
    # Clustered data
    c = []
    # Representatives
    representatives = []
    # Mean squared distance of the clustering
    accuracy = None

    # Constructor
    # Path to the dataset file (csv format)
    # K amount of clusters desired
    def __init__(self, path, k):
        self.path = path
        self.k = k

    # Reads the csv file and initializes the original_dataset
    # Features is a list of named features from the csv file you want to use in the model
    def read_csv(self, features):
        data = pd.read_csv(self.path)
        filtered_data = np.array([data[features[0]]]).T
        for i in range(1, len(features)):
            filtered_data = np.concatenate((filtered_data, np.array([data[features[i]]]).T), axis=1)
        self.original_dataset = filtered_data
    # Starts the clustering
    def start_clustering(self):
        print("Start clustering")
        print("Choosing initial representatives")
        self.__choose_initial_representatives()
        print(f"Initial representatives are:\n{self.representatives}")
        representatives_changed = False
        
        # Keep clustering until the representatives are fixed
        while(not representatives_changed):
            self.c = np.empty(len(self.original_dataset))
            print("Calculating distances")
            self.__calculate_distances()
            print("Recalculating representatives")
            representatives = self.__recalculate_representatives()
            compared = self.representatives == representatives
            representatives_changed = compared.all()
            self.representatives = representatives
            print(f"Representatives recalculated:\n{self.representatives}")
        self.__calculate_accuracy()
        print("Clustering ended")

    # Draws the scatter plot of the kmeans clustering
    # Xlabel label for X-axis
    # Xlim limit for X-axis, array form [from ,to]
    # Ylabel label for Y-axis
    # Ylim limit for Y-axis, array form [from, to]
    # Show show scatter plot at end of method, default = True
    def draw_scatter_plot(self, xlabel, ylabel, xlim, ylim, show=True):
        colors = ["red", "green", "yellow", "purple", "cyan", "blue"]
        x = []
        y = []
        for representative in self.representatives:
            x.append(representative[0])
            y.append(representative[1])
        for cluster in range(self.k):
            elements_x = []
            elements_y = []
            elements = np.where(self.c == cluster)
            element_cluster = np.array(self.original_dataset)[elements[0]]
            for element in element_cluster:
                elements_x.append(element[0])
                elements_y.append(element[1])
                plt.plot([element[0], x[cluster]], [element[1], y[cluster]], c=colors[int(cluster)], zorder=5)
            plt.scatter(elements_x, elements_y, c=colors[int(cluster)], label=f"Cluster {cluster}", zorder=0)
        plt.scatter(x, y, c="black", label=f"Representatives", zorder=10)
        plt.xlabel(xlabel)
        plt.xlim(xlim)
        plt.ylabel(ylabel)
        plt.ylim(ylim)
        plt.legend()
        if show:
            plt.show()

    # Method that choose K-unique representatives for the original dataset
    def __choose_initial_representatives(self):
        chosen_representatives = np.empty(shape=(self.k, len(self.original_dataset[0])))
        i = 0
        while i < self.k:
            chosen_representative = self.original_dataset[rd.randint(0, len(self.original_dataset) - 1)]

            # Choose unique representatives
            contains = np.where(chosen_representatives == chosen_representative)
            if len(contains[0]) == 0:
                chosen_representatives[i] = chosen_representative
                i += 1
        self.representatives = np.array(chosen_representatives)

    # Calculate the distance for each element to each representative and assigns a cluster
    def __calculate_distances(self):
        for element in range(len(self.original_dataset)):
            distances = np.empty(self.k)
            for k in range(self.k):
                distances[k] = sum((self.representatives[k] - self.original_dataset[element]) ** 2)
            
            # Assigns the element to a cluster for the lowest distance
            self.c[element] = np.argmin(distances)
        return distances
    
    # Calculates new representatives, mean from cluster it belongs to
    def __recalculate_representatives(self):
        representatives = np.zeros_like(self.representatives)
        for k in range(self.k):
            elements = np.where(self.c == k)
            avg = np.mean(np.array(self.original_dataset)[elements[0]], axis=0)
            representatives[k] = avg
        return representatives

    # Calculate the mean squared distance to each representative for each element in a cluster
    def __calculate_accuracy(self):
        total_accuracy = 0
        for cluster in range(self.k):
            cluster_accuracy = 0
            elements = np.where(self.c == cluster)
            for element in elements[0]:
                cluster_accuracy += sum(pow((self.representatives[cluster] - self.original_dataset[element]), 2))
            cluster_accuracy /= self.k
            total_accuracy += cluster_accuracy
        self.accuracy = total_accuracy