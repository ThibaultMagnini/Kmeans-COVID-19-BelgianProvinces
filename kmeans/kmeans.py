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
        features (list): The list with the names of all the features
        path (string): Path to the csv file for this model
        k (int): Amount of clusters for this model
    """
    original_dataset = []
    c = []
    representatives = []
    accuracy = None
    features = []

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
        self.features = features
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

    def draw_scatter_plot(self, xlim, ylim, show=True):
        """
        Draws the scatter plot of the kmeans clustering, should only be used when using 2 features in the model

        Args:
            xlim (list): Contains the from-to interval for the X-axis
            ylim (list): Contains the from-to interval for the Y-axis
            show (bool, optional): Defines if you want to show the plot at the end of the method. Defaults to True.

        Raises:
            Exception: Throws an exception when you try to call this method when you don't have 2 features
        """
        if len(self.features) != 2:
            raise Exception("To draw a 2d scatter plot you can only have 2 features")
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
        # The first feature will be on the X-axis
        plt.xlabel(self.features[0])
        plt.xlim(xlim)
        # The second feature will be on the Y-axis
        plt.ylabel(self.features[1])
        plt.ylim(ylim)
        plt.legend()
        if show:
            plt.show()

    def draw_scatter_plot_3d(self, show=True):
        """
        Draws the 3D scatter plot of the kmeans clustering, should only be used when using 3 features in the model

        Args:
            show (bool, optional): Defines if you want to show the plot at the end of the method. Defaults to True.

        Raises:
            Exception: Throws an exception when you try to call this method when you don't have 3 features
        """
        if len(self.features) != 3:
            raise Exception("To draw a 2d scatter plot you can only have 3 features")
        ax = plt.axes(projection='3d')
        ax.set_xlabel(self.features[0])
        ax.set_ylabel(self.features[1])
        ax.set_zlabel(self.features[2])
        colors = ["red", "green", "cyan", "purple", "yellow", "blue"]

        rep_x = []
        rep_y = []
        rep_z = []

        for cluster in range(self.k):
            elements_x = []
            elements_y = []
            elements_z = []
            elements = np.where(self.c == cluster)
            element_cluster = np.array(self.original_dataset)[elements[0]]
            for element in element_cluster:
                elements_x.append(element[0])
                elements_y.append(element[1])
                elements_z.append(element[2])
                ax.plot([element[0], self.representatives[cluster][0]], [element[1], self.representatives[cluster][1]], [element[2], self.representatives[cluster][2]], c=colors[cluster])
            ax.scatter3D(elements_x, elements_y, elements_z, c=colors[cluster], label=f"Cluster {cluster + 1}", alpha=1)
            rep_x.append(self.representatives[cluster][0])
            rep_y.append(self.representatives[cluster][1])
            rep_z.append(self.representatives[cluster][2])
        ax.scatter3D(rep_x, rep_y, rep_z, c="black", label="Representatives", alpha=1)
        ax.legend()
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

    def get_dataset_info(self):
        """
        Returns information about the dataset

        Returns:
            dict: Contains mean, stdev, max, min
        """
        mean = np.mean(self.original_dataset, axis=0)
        stdev = np.std(self.original_dataset, axis=0)
        maximum = np.amax(self.original_dataset, axis=0)
        minimum = np.amin(self.original_dataset, axis=0)
        return {"mean": mean, "stdev": stdev, "max": maximum, "min": minimum}

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
