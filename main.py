from Src import numbers
from numpy import delete, append, where
import multiprocessing as mp


def iter_k_times(n, k=150, prnt=False):
    r"""
    Iterates k times on some number n. If the digits in the sum of the digits
    of a number n exist in n then remove all occurences of that digit else
    append the digit to the end of n. Two end states will occur; a trajectory
    towards the empty set or a k0-state loop. k=150 is much larger than needed
    to prevent not accounting for extremely long runs/loops. The prnt variable
    can be used to print the trajectory. The function return the length of the
    trejectory, the starting number, and k0.
    """
    n = int(n)
    n_ori = n
    _temp = []
    for t in range(k):
        n_arr = numbers.num_to_arr(n)
        d_sum = sum(n_arr)
        d_arr = numbers.num_to_arr(d_sum)
        # Print Statement
        if prnt is True:
            print(n_arr, ' <--> ', d_arr)
        # Delete or Append element
        for value in d_arr:
            if value in n_arr:
                n_arr = delete(n_arr, where(n_arr == value))
            else:
                n_arr = append(n_arr, value)
        # Check for end state
        if len(n_arr) == 0:
            if prnt is True:
                print(n_arr, ' <--> ', [])
            return t, n_ori, 0
        n = numbers.arr_to_num(n_arr)
        # Check for k-state loops
        if n not in _temp:
            _temp.append(n)
        else:
            idx = _temp.index(n)
            k = len(_temp) - idx
            if prnt is True:
                d_sum = sum(n_arr)
                d_arr = numbers.num_to_arr(d_sum)
                print(n_arr, ' <--> ', d_arr)
            return -1, n_ori, k
    return -1, n_ori, 0


def search_parallel():
    # 7999999 largest run of 24 - 8/24/2020
    # 2999999 largest loop of 4  - 8/24/2020
    cpu = 8
    largest_t = 0
    largest_n = 0
    largest_l = 0
    largest_loop_n = 0
    max_n = pow(10, 6)
    min_n = pow(10, 0)
    size = max_n // (2*cpu)
    with mp.Pool(processes=cpu) as pool:
        for x in range(0, 100):
            data = [i for i in range(min_n + x*max_n, max_n + x*max_n)]
            for result in pool.imap_unordered(iter_k_times, data, chunksize=size):
                if result[0] != -1:
                    if result[0] > largest_t:
                        largest_t = result[0]
                        largest_n = result[1]
                else:
                    if result[2] > largest_l:
                        largest_l = result[2]
                        largest_loop_n = result[1]
        print('\n')
        print(largest_n, largest_t, 'RUN\n')
        iter_k_times(largest_n, prnt=True)
        print('\n')
        print(largest_loop_n, largest_l, 'LOOP\n')
        iter_k_times(largest_loop_n, prnt=True)
        print('\n')


if __name__ == "__main__":
    # search_parallel()
    iter_k_times(7999999, prnt=True)
