import os
import numpy as np

"""
    Contains problem-specific logic for reading the input and writing the output
"""

# Problem-specific ID
PROBLEM_ID = '6417837228818432'

# List of problem-specific input filenames, and associated dataset ID
INPUT_FILENAMES = {
    # 'a_example.txt': '6199627120377856',
    # 'b_lovely_landscapes.txt': '5239399268745216',
    # 'c_memorable_moments.txt': '5185683152961536',
    # 'd_pet_pictures.txt': '6378347655331840',
    'e_shiny_selfies.txt': '4834468208574464',
}

def transform_strings(photos):
    seen = set()
    for line in photos:
        seen |= set(line[1])

    inverse_d = {x:i for i,x in enumerate(seen)}
    for line in photos:
        line[1] = set([inverse_d[l] for l in line[1]])

    return photos

def read_input(filename):
    """
        Example input reader for the 'Slideshow' problem.
        Returns a tuple of:
            N:      Number of photos
            photos: list of Photo, where a Photo is:
                - 0 for horizontal, 1 for vertical
                - a list of words
    """
    with open(filename, 'r') as f:
        (N) = map(int, next(f).split())
        def parse_line(line):
            l = line.split()
            h = 0 if l[0] == 'H' else 1
            n = int(l[1])
            return [h, l[2:]]

        photos = transform_strings([parse_line(line) for line in f])
        return (len(photos), photos)

def get_transitions_scores(input_data, output_data):
    N, photos = input_data
    slides = output_data

    transition_scores = []
    for i in range(len(slides) - 1):
        photos1 = slides[i]
        keywords1 = set()
        for p in photos1:
            keywords1 |= photos[p][1]
        photos2 = slides[i+1]
        keywords2 = set()
        for p in photos2:
            keywords2 |= photos[p][1]

        num_inter = len(keywords1.intersection(keywords2))
        num_1_minus_2 = len(keywords1.difference(keywords2))
        num_2_minus_1 = len(keywords2.difference(keywords1))
        transition_scores.append(min(num_inter, num_1_minus_2, num_2_minus_1))

    return transition_scores

def score_pair(t1, t2):
    inter = t1.intersection(t2)
    return min(len(inter), len(t1.difference(inter)), len(t2.difference(inter)))

def evaluate(input_data, output_data):
    """
        Example output evaluation for the 'Slideshow' problem.
     """
    transition_scores = get_transitions_scores(input_data, output_data)

    return True, sum(transition_scores)

def write_output(filename, output_data):
    """
        Example output writer for the 'Slideshow' problem.
        Input data is a list of slide, where each slide is a list of photos.
    """
    folder = os.path.dirname(filename)
    if not os.path.exists(folder):
        os.mkdir(folder)

    with open(filename, 'w') as f:
        f.write(str(len(output_data)) + '\n')
        for slide in output_data:
            f.write(' '.join(map(str, slide)) + '\n')
