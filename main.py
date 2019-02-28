import copy
import numpy as np
from random import shuffle
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
    verticals = [[i, lines[i][1]] for i in range(len(lines)) if lines[i][0] == 1]
    verticals = sort_verticals(verticals)
    result = [[i] for i in range(len(lines)) if lines[i][0] == 0] + verticals
    return result

def find_index_best(tags, verticals):
    lim = 100
    if len(verticals) < lim:
        return 0
    for i in range(lim):
        if tags.intersection(verticals[i][1]) == 0:
            return i
    return 0

def sort_verticals(verticals):
    couples = []
    while len(verticals):
        element = verticals.pop()
        index = find_index_best(element[1], verticals)
        couple = verticals[index][0]
        couples.append([element[0], couple])
        del verticals[index]

    return couples

def paul_solution(input_data):
    (N, photos) = copy.deepcopy(input_data)
    solution = [[i] for i in range(len(photos)) if photos[i][0] == 0]

    V_photos = [i for i in range(len(photos)) if photos[i][0] == 1]
    V_photos = [[V_photos[2*i], V_photos[2*i+1]] for i in range(int(len(V_photos)/2))] # merge
    H_photos = [[i] for i in range(len(photos)) if photos[i][0] == 0]

    solution = H_photos + V_photos
    transitions_scores = utils.processing.get_transitions_scores(input_data, solution)

    return solution

if __name__ == '__main__':
    utils.run_solution(my_solution)
