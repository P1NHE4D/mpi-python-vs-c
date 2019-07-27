# About this project
This project compares the performance of mpi in python and mpi in c. The comparison is based on a simple algorithm that calculates the average of the elements in an integer array. The results were quite impressive. Even though I used the optimized functions to transfer buffer-like objects only in order to reduce overhead as much as possible, python was significantly slower than C. 

Additionally, I've implemented a parallel merge sort algorithm to illustrate the boost in performance that can be achieved by 
implementing a parallel algorithm rather than a serial algorithm. 
