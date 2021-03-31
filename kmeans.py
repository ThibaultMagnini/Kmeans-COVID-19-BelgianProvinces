import numpy as np
import pandas as pd
import random as rd
import matplotlib.pyplot as plt


class Kmeans:
    """
    A class to represent a kmeans clustering

    Attributes:
        original_dataset (list): Contains the data from the original dataset
        c (list): Contains the information about which element belongs to which cluster
        representatives (list): Contains the representatives for the clustering
        accuracy (float): The mean squared distance for the model
        path (string): Path to the csv file for this model
        k (int): Amount of clusters for this model
    """
    original_dataset = []
    c = []
    representatives = []
    accuracy = None

    def __init__(self, path, k):
        """
        Constructs all the necessary attributes for the kmeans object

        Args:
            path (string): Path to the csv file for this model
            k (int): Amount of clusters for this model
        """
        self.path = path
        self.k = k

    def read_csv(self, features):
        """
        Reads the csv file and initializes the original_dataset

        Args:
            features (list): List of named features from the csv file that you want to use in the model
        """
        data = pd.read_csv(self.path)
        filtered_data = np.array([data[features[0]]]).T
        for i in range(1, len(features)):
            filtered_data = np.concatenate((filtered_data, np.array([data[features[i]]]).T), axis=1)
        self.original_dataset = filtered_data

    def start_clustering(self):
        """
        Starts the clustering
        """
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

    def draw_scatter_plot(self, xlabel, ylabel, xlim, ylim, show=True):
        """
        Draws the scatter plot of the kmeans clustering, should only be used when using 2 features in the model

        Args:
            xlabel (string): label for the X-axis
            ylabel (string): label for the Y-axis
            xlim (list): Contains the from-to interval for the X-axis
            ylim (list): Contains the from-to interval for the Y-axis
            show (bool, optional): Defines if you want to show the plot at the end of the method. Defaults to True.
        """
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

    def get_clusters_info(self):
        """
        Returns information about each clusters features

        Returns:
            dict: Contains mean, stdev, max, min
        """
        result = {}
        for cluster in range(self.k):
            elements = np.where(self.c == cluster)
            element_cluster = np.array(self.original_dataset)[elements[0]]
            mean = np.mean(element_cluster, axis=0)
            stdev = np.std(element_cluster, axis=0)
            maximum = np.amax(element_cluster, axis=0)
            minimum = np.amin(element_cluster, axis=0)
            result[cluster] = {"mean": mean, "stdev": stdev, "max": maximum, "min": minimum}
        return result

    def __choose_initial_representatives(self):
        """
        Method that choose K-unique representatives for the original dataset
        """
        chosen_representatives = np.empty(
            shape=(self.k, len(self.original_dataset[0])))
        i = 0
        while i < self.k:
            chosen_representative = self.original_dataset[rd.randint(0, len(self.original_dataset) - 1)]

            # Choose unique representatives
            contains = np.where(chosen_representatives == chosen_representative)
            if len(contains[0]) == 0:
                chosen_representatives[i] = chosen_representative
                i += 1
        self.representatives = np.array(chosen_representatives)

    def __calculate_distances(self):
        """
        Calculate the distance for each element to each representative and assigns a cluster
        """
        for element in range(len(self.original_dataset)):
            distances = np.empty(self.k)
            for k in range(self.k):
                distances[k] = sum((self.representatives[k] - self.original_dataset[element]) ** 2)

            # Assigns the element to a cluster for the lowest distance
            self.c[element] = np.argmin(distances)

    def __recalculate_representatives(self):
        """
        Calculates new representatives, mean from cluster it belongs to

        Returns:
            list: Contains the new representative for each cluster
        """
        representatives = np.zeros_like(self.representatives)
        for k in range(self.k):
            elements = np.where(self.c == k)
            avg = np.mean(np.array(self.original_dataset)[elements[0]], axis=0)
            representatives[k] = avg
        return representatives

    def __calculate_accuracy(self):
        """
        Calculate the mean squared distance to each representative for each element in a cluster
        """
        total_accuracy = 0
        for cluster in range(self.k):
            cluster_accuracy = 0
            elements = np.where(self.c == cluster)
            for element in elements[0]:
                cluster_accuracy += sum(
                    pow((self.representatives[cluster] - self.original_dataset[element]), 2))
            cluster_accuracy /= self.k
            total_accuracy += cluster_accuracy
        self.accuracy = total_accuracy
