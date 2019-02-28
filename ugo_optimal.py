import copy
import numpy as np
from random import shuffle
import utils
from scipy.stats import describe
import pickle

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
    threshold = stats.mean-2
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
    with open('temp_d.pkl', 'rb') as f:
          solution = pickle.load(f)

    print_metrics(input_data, solution)

    photo_scores, transitions_scores = get_scores(input_data, solution)
    stats = describe(photo_scores)
    good_photos = np.where(photo_scores > stats.mean-2)[0]
    bad_photos = np.where(photo_scores <= stats.mean-2)[0]
    print(bad_photos.shape[0])

    photos = np.concatenate((good_photos, bad_photos))
    solution = [solution[photos[i]] for i in photos]
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
