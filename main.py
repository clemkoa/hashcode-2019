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
    (R, C, L, H, lines) = copy.deepcopy(input_data)
    solution = []
    for i in range(R):
        for j in range(C):
            if is_slice_valid(lines, i, j, i + H - 1, j, R, C, L, H):
                solution.append([i, j, i + H - 1, j])
                lines[i:i+H, j:j+1] = 2
    return solution

if __name__ == '__main__':
    utils.run_solution(my_solution, local_only=True)
