import copy
import pickle
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
    a = [[i] for i in range(len(lines)) if lines[i][0] == 0] + verticals
    a.sort(key=lambda x: sum(list(map(lambda y: len(lines[y][1]), x))), reverse=True)
    res = construct_results(a, lines)
    return res

def get_keywords(photo, lines):
    if len(photo) == 2:
        return lines[photo[0]][1].union(lines[photo[1]][1])
    return lines[photo[0]][1]

def pair_score(photo1, photo2, lines):
    keywords1 = get_keywords(photo1, lines)
    keywords2 = get_keywords(photo2, lines)
    num_inter = len(keywords1.intersection(keywords2))
    num_1_minus_2 = len(keywords1.difference(keywords2))
    num_2_minus_1 = len(keywords2.difference(keywords1))
    return min(num_inter, num_1_minus_2, num_2_minus_1)

def construct_results(photos, lines):
    element = photos.pop()
    results = [element]
    while len(photos) > 0:
        print(len(photos))
        index = find_index_best_pair(element, photos, lines)
        results.append(photos[index])
        element = copy.copy(photos[index])
        del photos[index]
    return results

def find_index_best_pair(photo, photos, lines):
    lim = 20
    for m in range(len(get_keywords(photo, lines)), 0, -1):
        for i in range(min(len(photos), lim)):
            if pair_score(photo, photos[i], lines) > m:
                return i
    return 0

def find_index_best(tags, verticals):
    lim = 300
    if len(verticals) < lim:
        return 0
    for i in range(lim):
        if tags.intersection(verticals[i][1]) == 0:
            return i
    return 0

def sort_verticals(verticals):
    couples = []
    while len(verticals) > 2:
        element = verticals.pop()
        index = find_index_best(element[1], verticals)
        couple = verticals[index][0]
        couples.append([element[0], couple])
        del verticals[index]
    print('verticals done')
    return couples

if __name__ == '__main__':
    utils.run_solution(my_solution)
