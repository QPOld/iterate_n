from numpy import asarray


def num_to_arr(number):
    n = int(number)
    arr = [int(x) for x in str(n)]
    return asarray(arr, dtype=int)


def arr_to_num(arr):
    _str = ''
    for val in arr:
        _str += str(val)
    return int(_str)
