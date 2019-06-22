import sys
from mpi4py import MPI
import numpy as np
import time


comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()


def main():
    a_size = 0
    array = None

    # Set a_size and generate array
    if rank == 0:
        a_size = int(input(f'Enter the desired size of the array: '))
        array = np.random.randint(-100000, 100000, a_size * size, dtype='i')

    # Broadcast a_size to all processes, set recvbuf
    a_size = comm.bcast(a_size, root=0)
    start = time.time()
    recvbuf = np.zeros(a_size, dtype='i')

    # Distribute data and calculate average of sub-array
    comm.Scatter(array, recvbuf, root=0)
    avg = calc_avg(recvbuf)

    # Calculate calculation time of worker processes
    if rank != 0:
        stop = time.time() - start
        print(f'Task: {rank} | Average: {avg} | Calc_time: {stop} sec.')
        sys.stdout.flush()

    # Gather data
    ls = comm.gather(avg, root=0)

    if rank == 0:
        # Calculate total average
        total_avg = calc_avg(ls)
        stop = time.time() - start
        print(f'Parallel calculation | Total average: {total_avg} | Total Calc_time: {stop} sec.')
        sys.stdout.flush()

        # Serial calculation
        serial_start = time.time()
        avg = calc_avg(array)
        serial_stop = time.time() - serial_start
        print(f'Serial calculation | Total avg: {avg} | Calc_time: {serial_stop} sec.')


# Calculates the average of the elements in an array
def calc_avg(array):
    total = 0
    for i in range(0, len(array)-1):
        total = total + array[i]
    return total / len(array)


if __name__ == '__main__':
    main()
