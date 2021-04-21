# Kmeans-COVID-19-BelgianProvinces

Jonas and I are currently researching provincial clustering in Belgium during the COVID-19 Pandemic.
This way we can cluster belgian provinces in regions of severity to provide guidance and insights into which regions should get priority in the vaccination strategy.
This research is in collaboration with *Sao Paulo State University- The Universidade Estadual Paulista (UNESP)*

Given the Governement Dataset we are looking for the correct parameters to cluster the different belgian provinces.
This way we can find in what regions COVID-19 has had a bigger impact and also provide insights on what regions are more vulnerable and need more guidance/help.

Some of the results/graphs can be found in /Results .
These are some intermediate results which are current applications of our clustering algorithm.

## K means clustering algoritm

This research is based on the k-means clustering algorithm.

It was run several times with different predefined number of clusters, K.
We calculate the sum mean squared within every cluster to check cluster validity and chose the optimal amount of clusters.
The k-means clustering algoritm will iterate until convergence of the cluster centroids/representatives. 

