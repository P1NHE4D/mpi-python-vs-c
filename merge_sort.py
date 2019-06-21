from mpi4py import MPI
import numpy as np
import sys
import time


def parallel_sort():
    comm = MPI.COMM_WORLD
    size = comm.Get_size()
    rank = comm.Get_rank()

    if rank == 0:
        a_size = int(input('Please enter the size of the array: '))
        print(f'Generating random array with {a_size} elements...')
        sys.stdout.flush()  # forces stdout to flush its buffer immediately
        array = np.random.randint(-100000, 100000, size=a_size, dtype='i')

        print('Performing parallel sort...')
        sys.stdout.flush()
        oh_start = time.time()
        calc_start = time.time()

        # Bisect array
        middle = array.size // 2
        send_data = array[:middle]
        local_data = array[middle:]

        # Distribute data
        comm.Send([send_data, MPI.INT], dest=1, tag=10)
        oh_stop = time.time() - oh_start

        # Sort local data
        local_data = np.array(merge_sort(local_data))

        # Receive remote data
        oh_start = time.time()
        info = MPI.Status()
        comm.Probe(MPI.ANY_SOURCE, MPI.ANY_TAG, info)
        count = info.Get_elements(MPI.INT)
        recv_data = np.zeros(count, dtype='i')
        comm.Recv(recv_data, MPI.ANY_SOURCE, MPI.ANY_TAG)
        oh_stop = oh_stop + (time.time() - oh_start)

        # Merge local and remote data
        local_data = list(local_data)
        recv_data = list(recv_data)
        sorted_arr = merge(local_data, recv_data)
        calc_stop = time.time() - calc_start
        print(f'Parallel sort: {calc_stop} seconds')
        print(f'Overhead:      {oh_stop} seconds ({round((oh_stop / calc_stop) * 100, 2)}%)')
        print('Performing serial sort...')
        sys.stdout.flush()

        # perform serial sort
        scalc_start = time.time()
        merge_sort(array)
        scalc_stop = time.time() - scalc_start
        print(f'Serial sort:   {scalc_stop} seconds')
        if scalc_stop > calc_stop:
            print(f'Parallel sort was {round((1 - (calc_stop / scalc_stop)) * 100, 2)}% '
                  f'faster than serial sort')
        else:
            print(f'Serial sort was {round((1 - (scalc_stop / calc_stop)) * 100, 2)}% '
                  'faster than parallel sort')

    elif rank == 1:
        # get size of remote data
        info = MPI.Status()
        comm.Probe(MPI.ANY_SOURCE, MPI.ANY_TAG, info)
        count = info.Get_elements(MPI.INT)

        # receive remote data
        local_data = np.zeros(count, dtype='i')
        comm.Recv(local_data, MPI.ANY_SOURCE, MPI.ANY_TAG)

        # sort data
        send_data = np.array(merge_sort(local_data), dtype='i')

        # send sorted data
        comm.Send([send_data, MPI.INT], dest=0)


def merge(left, right):
    result = []
    left_index = 0
    right_index = 0

    # compare the elements of each list
    while left_index < len(left) and right_index < len(right):
        if left[left_index] <= right[right_index]:
            result.append(left[left_index])
            left_index += 1
        else:
            result.append(right[right_index])
            right_index += 1

    # append the remaining parts of the array
    if left:
        result.extend(left[left_index:])
    if right:
        result.extend(right[right_index:])

    return result


def merge_sort(array):
    if len(array) <= 1:
        return array

    middle = len(array) // 2  # // is floor division
    left = array[:middle]  # [:] means slicing - e.g. [2:4] from 2 to 3, as it is right exclusive
    right = array[middle:]

    left = merge_sort(left)
    right = merge_sort(right)
    return list(merge(left, right))


if __name__ == '__main__':
    globals()[sys.argv[1]]()
