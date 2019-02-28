import copy
import numpy as np
from random import shuffle
import utils
from scipy.stats import describe

from utils.processing import score_pair
from main import my_solution

def get_scores(input_data, solution):
    transitions_scores = np.array(utils.processing.get_transitions_scores(input_data, solution))

    photo_scores = transitions_scores[1:] + transitions_scores[:-1]
    photo_scores = np.insert(photo_scores, 0, transitions_scores[0])
    photo_scores = np.insert(photo_scores, -1, transitions_scores[-1])

    return photo_scores, transitions_scores

def print_metrics(input_data, solution):
    photo_scores, transitions_scores = get_scores(input_data, solution)
    score = sum(transitions_scores)
    num_zeros = np.where(transitions_scores == 0)[0].shape[0]
    print('{:#^10}'.format(''))
    print('Transition score: {}'.format(score))
    print('Transition describe: {}'.format(describe(transitions_scores)))
    print('Transition that score 0: {}'.format(num_zeros))
    print('Photo describe: {}'.format(describe(photo_scores)))

def get_best(p1, to_pick):
    depth = min(1000, len(to_pick))
    argmax = np.argmax(np.array([score_pair(p1[1], to_pick[i][1]) for i in range(depth)]))
    p2 = to_pick[argmax]
    del to_pick[argmax]
    return p2

def get_best_worst(p2_1, p1_1, to_pick):
    depth = min(1000, len(to_pick))
    argmax = np.argmax(np.array([score_pair(p2_1[1], to_pick[i][1]) for i in range(depth)]) \
            - np.array([score_pair(p1_1[1], to_pick[i][1]) for i in range(depth)]))

    p1_2 = to_pick[argmax]
    del to_pick[argmax]
    return p1_2

def get_twice_best(p1_1, p1_2, to_pick):
    depth = min(1000, len(to_pick))
    argmax = np.argmax(np.array([score_pair(p1_1[1], to_pick[i][1]) for i in range(depth)]) \
            + np.array([score_pair(p1_2[1], to_pick[i][1]) for i in range(depth)]))
    p2 = to_pick[argmax]
    del to_pick[argmax]
    return p2

def get_twice_best_worst(p1_1, p1_2, p2_1, to_pick):
    depth = min(1000, len(to_pick))
    argmax = np.argmax(np.array([score_pair(p1_1[1], to_pick[i][1]) for i in range(depth)]) \
            + np.array([score_pair(p1_2[1], to_pick[i][1]) for i in range(depth)]) \
            - np.array([score_pair(p2_1[1], to_pick[i][1]) for i in range(depth)]))

    p2_2 = to_pick[argmax]
    del to_pick[argmax]
    return p2_2

def paul_e(input_data):
    (N, photos) = copy.deepcopy(input_data)

    to_pick = copy.deepcopy(photos)

    solution = []

    for i in range(len(to_pick)):
        to_pick[i][0] = i

    first = True
    while len(to_pick) != 0:
        if first:
            p1_1 = to_pick.pop()
            p2_1 = get_best(p1_1, to_pick)
            p1_2 = get_best_worst(p2_1, p1_1, to_pick)
            p2_2 = get_twice_best_worst(p1_1, p1_2, p2_1, to_pick)
            solution.append([p1_1[0], p1_2[0]])
            solution.append([p2_1[0], p2_2[0]])

            p1_1 = p2_1
            p1_2 = p2_2
            first = False
        else:
            p2_1 = get_twice_best(p1_1, p1_2, to_pick)
            p2_2 = get_twice_best_worst(p1_1, p1_2, p2_1, to_pick)
            solution.append([p2_1[0], p2_2[0]])

        if len(solution)%10000 == 0:
            print(len(solution))
            print_metrics(input_data, solution)
    print_metrics(input_data, solution)

    return solution

if __name__ == '__main__':
    utils.run_solution(paul_e)
