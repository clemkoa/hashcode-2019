import numpy as np
import os

import utils

def read(INPUT_FOLDER, file_name):
    path = os.path.join('input', file_name)
    with open(path, 'r') as f:
        R, C, L, H = map(int, next(f).split())

        def parse_line(line):
            return [0 if c is 'M' else 1 for c in line]

        lines = np.array([parse_line(line) for line in f])
        return R, C, L, H, lines

def write(path, solution):
    folder = os.path.dirname(path)
    if not os.path.exists(folder):
        os.mkdir(folder)

    with open(path, 'w') as f:
        f.write(str(len(solution)) + '\n')
        for rect in solution:
            f.write(' '.join(map(str, rect)) + '\n')

def is_slice_valid(pizza, xmin, ymin, xmax, ymax, R, C, L, H):
    slice = pizza[xmin:xmax + 1, ymin:ymax + 1]
    if xmax >= R - 1: return False
    if ymax >= C - 1: return False
    if 2 in slice: return False
    if np.sum(slice) >= L and slice.size - np.sum(slice) >= L and slice.size <= H:
        return True
    return False

def build_solution(R, C, L, H, lines):
    solution = []
    for i in range(R):
        for j in range(C):
            if is_slice_valid(lines, i, j, i + H - 1, j, R, C, L, H):
                solution.append([i, j, i + H - 1, j])
                lines[i:i+H, j:j+1] = 2
    return solution

if __name__ == '__main__':
    INPUT_FOLDER = 'input'
    OUTPUT_FOLDER = 'output'
    utils.zip_code()
    files = os.listdir(INPUT_FOLDER)
    for file in files:
        print(file)
        R, C, L, H, lines = read(INPUT_FOLDER, file)
        solution = build_solution(R, C, L, H, lines)
        print(solution)
        write(os.path.join(OUTPUT_FOLDER, file), solution)
