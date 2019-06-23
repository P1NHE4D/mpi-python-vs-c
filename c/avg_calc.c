#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include </usr/local/Cellar/mpich/3.3.1/include/mpi.h>

//function declaration
double calc_avg(int array[], int size);
int * rand_int(int size);

int main(int argc, char** argv) {

    MPI_Init(NULL, NULL);
    srand(time(NULL));

    int rank;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    int size;
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    int a_size = 10000000;
    int *arr = NULL;
    clock_t start, stop;
    double calc_time;

    // Generate random array
    if (rank == 0) {
        printf("Array size: %d \n", a_size);
        arr = rand_int(a_size * size);
    }

    start = clock();
    // Initialize buffer
    int *recv_buf = malloc(sizeof(int) * a_size);

    // Scatter data
    MPI_Scatter(arr, a_size, MPI_INT, recv_buf, a_size, MPI_INT, 0, MPI_COMM_WORLD);

    // Calculate average of sub-array
    double avg;
    avg = calc_avg(recv_buf, a_size);
    printf("Average of sub-array %f \n", avg);

    // Gather averages of sub-arrays
    double *avgs = NULL;
    if (rank == 0) {
        avgs = malloc(sizeof(double) * size);
    }
    MPI_Gather(&avg, 1, MPI_DOUBLE, avgs, 1, MPI_DOUBLE, 0, MPI_COMM_WORLD);

    // Calculate total average
    if (rank == 0) {
        double total_avg;
        double sum = 0;
        for(int i = 0; i < size; ++i) {
            sum = sum + avgs[i];
        }
        total_avg = sum / size;
        stop = clock();
        calc_time = ((double) (stop - start)) / CLOCKS_PER_SEC;
        printf("Total avg: %f | calc_time: %f sec. \n", total_avg, calc_time);
    }

    MPI_Finalize();

}

// Calculates the average of the elements in an array
double calc_avg(int array[], int size) {
    int sum = 0;
    for(int i = 0; i < size; ++i) {
        sum = sum + array[i];
    }
    return (double) sum / size;
}

// Generates a random array of size in range min and max (inclusive)
int * rand_int(int size) {
    int *arr = malloc(sizeof(int)*size);
    for (int i = 0; i < size; ++i) {
        arr[i] = (rand() % 11) ;
    }
    return arr;
}