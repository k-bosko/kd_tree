# Measuring the performance of KD Trees for solving the nearest neighbor problem

**Authors**:  Katerina Bosko, Thean Lim, Mubarak Nsamba, Amit Pai 

Final Project for CS5800 Algorithms class at the Northeastern University

## Project Description

The Nearest Neighbor Problem is the problem of finding the point in a dataset that is closest to a given query point. The generalized k-Nearest Neighbors algorithm (KNN) that finds k-number of most similar points is very popular in Machine Learning for classification tasks. There are many algorithms for solving the nearest neighbor problem. In this project, we explored one of them - the KD Tree algorithm. Developed by Jon Louis Bentley in 1975, KD Tree has been widely adopted due to its simplicity and efficiency and is used in different fields Clustering, Recommendation, Computer Vision, and many others.

The project’s scope:
- To implement KD Tree algorithm
- To test the implementation on an image dataset
- To measure the performance of KD Tree versus the naive approach

## Testing KD Tree implementation

The KD-Tree implementation was tested using the image recoloring approach. This involves mapping the colors of an input image to a specified color palette, which can be formulated as finding the nearest neighbor for each pixel's color from the set of colors in the palette. The output of the algorithm is a recolored version of the input image.

To implement the recoloring approach, we need
1) color palettes <br>
We created seven color palettes that contain 128, 256, 512, 1024, 2048, 4096, and 8192 colors. Each bigger color palette contains a subset of smaller color palettes. The colors were selected from the whole universe of possible RGB colors, which is 256x256x256 or about 16,78 million colors.
2) input image <br>
As an input image, a squared color wheel was chosen because it contains 68,850 unique colors equally distributed across RGB color channels. Choosing an image with a very high number of unique colors ensures that the algorithm will calculate a high number of unique distances, which is desired in order to see the differences in performance.

## Nearest neighbor problem formulation
In this formulation of the nearest neighbor problem as a recoloring problem, the “nearest” is judged by the Euclidean distances between colors. For instance, if we have two colors - paletteColor: [13, 57, 71] and imgColor [194, 191, 186], the distance between them is:


## KD Tree implementation benchmarks
We compare the performance of our KD-Tree implementation against two other benchmarks:
- the Naive algorithm: finds the minimum distance for each pixel’s color by brute force iteration through each color in a color palette
- Scipy algorithm: the KD-Tree implementation from the scipy library in Python, which is one of the primary libraries for scientific computing.

All algorithms were implemented in Python and are called converters that extend the BaseConverter class:
- NaiveConverter
- ScipyKDTreeConverter
- CustomKDTreeConverter 

A script was written in Python to automate the task of measuring the performance of all three converters, each running on seven different color palettes.


## Operationalization of performance
The algorithm’s performance was measured by timing how long it took to find the nearest neighbor for each pixel’s color from the color palette. Given that we have 7 color palettes and 3 algorithms, this results in 21 different measurements. perf_counter() was used as a timing function before starting the search and immediately after the search was finished. The final time elapsed is the difference between starting and ending time. 

## Results

