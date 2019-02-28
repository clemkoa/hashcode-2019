import copy

from json import dump

from collections import defaultdict
from random import shuffle, sample

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

def score_pair(t1, t2):
    inter = t1.intersection(t2)
    return min(len(inter), len(t1.difference(inter)), len(t2.difference(inter)))

def compute_friends(tags, reverse):
    return [set(r for t in tag for r in reverse[t]) for tag in tags]

def reverse_tags(tags):
    reverse = defaultdict(set)
    for i, tag in enumerate(tags):
        for t in tag:
            reverse[t].add(i)
    return reverse

def my_solution(input_data):
    (N, photos) = copy.deepcopy(input_data)

    slides = starting(photos)
    tags = update_tags(slides, photos)

    reverse = reverse_tags(tags)
    friends = compute_friends(tags, reverse)

    all_slides = set(range(len(friends)))
    path = [0]
    path_set = set([0])
    total = 0
    for a in range(len(friends) - 1):
        current = path[-1]
        scores = [(score_pair(tags[current], tags[f]), f) for f in friends[current]]
        if len(scores) == 0:
            next_slide = sample(path_set.intersection(all_slides), 1)[0]
            score = 0
        else:
            (score, next_slide) = max(scores)

        total += score
        # print(a, total, score, current, next_slide, tags[current].intersection(tags[next_slide]))
        print(a, total, score)

        path.append(next_slide)
        path_set.add(next_slide)

        for i in range(len(friends)):
            if next_slide in friends[i]:
                friends[i].remove(next_slide)

    final = [slides[i] for i in path]

    with open('path.out', 'w') as f:
        dump(path, f)
    with open('final.out', 'w') as f:
        dump(path, f)

    print('Final: ' + str(len(path)))

    return final

    # print(slides)
    # print(tags)
    # print(dict(reverse))
    # print(friends)

    return slides

if __name__ == '__main__':
    utils.run_solution(my_solution)
