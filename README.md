# Kmeans-COVID-19-BelgianProvinces

Jonas and I are currently researching provincial clustering in Belgium during the COVID-19 Pandemic.
This way we can cluster belgian provinces in regions of severity to provide guidance and insights into which regions should get priority in the vaccination strategy.
Next to that we try to apply different SIR-Model Variations on the belgian COVID-19 data using Neural Networks to forecast the spread of the Virus.
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

## SIR Epidemiological model with continious Beta 

To expand our research we decided to implement some trend analysis/forecast using the most basic form of the SIR model.
Using this Ordinary Differential equation the spread of a disease can be visualised and further development of the Beta and Gamma parameters can be detirment.

In our first case SIR was used with a continious Beta (Infection Rate). We used Non-Linear least squares fitting to fit the SIR-model parameters on the actual belgian data.
This lead to some basic forecasts with acceptable accuracy.

## SIR Epidemiological model with Transient Beta Using Neural Networks

In this step of our research we used Machine Learning technology to make more accurate predictions using A transient Beta parameter.
This Beta parameter is estimated by the ANN implemented in python. 
Having the Sigmoid kernel as the network activation function.
And having ReLU as activation function on the output layer, existing of a Single neuron
