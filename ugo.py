import copy
import numpy as np
from random import shuffle
import utils
from scipy.stats import describe

from main import my_solution

def get_scores(input_data, solution):
    transitions_scores = np.array(utils.processing.get_transitions_scores(input_data, solution))

    photo_scores = transitions_scores[1:] + transitions_scores[:-1]
    photo_scores = np.insert(photo_scores, 0, transitions_scores[0])
    photo_scores = np.insert(photo_scores, -1, transitions_scores[-1])

    return photo_scores, transitions_scores

def better_solution(input_data, solution, iter):
    photo_scores, transitions_scores = get_scores(input_data, solution)
    photos = np.arange(len(solution))
    stats = describe(photo_scores)
    threshold = stats.mean#min(stats.mean, stats.mean * (iter / 100))
    if iter%10 == 0:
        print('thres: {}'.format(threshold))
    zero_ids = np.where(photo_scores <= threshold)[0]
    photos[zero_ids] = np.random.permutation(photos[zero_ids])

    return [solution[photos[i]] for i in photos]

def print_metrics(input_data, solution):
    photo_scores, transitions_scores = get_scores(input_data, solution)
    score = sum(transitions_scores)
    num_zeros = np.where(transitions_scores == 0)[0].shape[0]
    print('{:#^10}'.format(''))
    print('Transition score: {}'.format(score))
    print('Transition describe: {}'.format(describe(transitions_scores)))
    print('Transition that score 0: {}'.format(num_zeros))
    print('Photo describe: {}'.format(describe(photo_scores)))

def paul_solution(input_data):
    (N, photos) = copy.deepcopy(input_data)
    solution = my_solution(input_data)
    print('Jood done')


    print_metrics(input_data, solution)

    for iter in range(100):

        solution = better_solution(input_data, solution, iter)
        if iter%10 == 0:
            transitions_scores = utils.processing.get_transitions_scores(input_data, solution)
            score = sum(transitions_scores)
            num_zeros = np.where(transitions_scores == 0)[0].shape[0]
            print_metrics(input_data, solution)

    print_metrics(input_data, solution)

    return solution

if __name__ == '__main__':
    utils.run_solution(paul_solution)
