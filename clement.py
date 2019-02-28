import copy

from random import shuffle

import numpy as np

import utils

def starting(photos):
    verticals = [i for i, (is_v, _) in enumerate(photos) if is_v]
    permuted = np.random.permutation(verticals)
    groups = [[permuted[i * 2], permuted[(i * 2) + 1]] for i in range(len(permuted) // 2)]
    horizontals = [[i] for i, (is_v, _) in enumerate(photos) if not is_v]
    path = groups + horizontals
    shuffle(path)
    return path

def update_tags(slides, photos):
    tags = [photos[ids[0]][1] if len(ids) == 1 else photos[ids[0]][1].union(photos[ids[1]][1]) for ids in slides]
    return tags

def my_solution(input_data):
    (N, photos) = copy.deepcopy(input_data)

    slides = starting(photos)
    tags = update_tags(slides, photos)
    compute_distances(slides, tags)

    return slides

if __name__ == '__main__':
    utils.run_solution(my_solution)
