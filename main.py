import copy
import numpy as np

import utils

def is_slice_valid(pizza, xmin, ymin, xmax, ymax, R, C, L, H):
    slice = pizza[xmin:xmax + 1, ymin:ymax + 1]
    if xmax >= R - 1: return False
    if ymax >= C - 1: return False
    if 2 in slice: return False
    if np.sum(slice) >= L and slice.size - np.sum(slice) >= L and slice.size <= H:
        return True
    return False

def my_solution(input_data):
    (N, lines) = copy.deepcopy(input_data)
    solution = []
    return [[i] for i in range(len(lines)) if lines[i][0] == 0]

if __name__ == '__main__':
    utils.run_solution(my_solution)
