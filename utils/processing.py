import os
import numpy as np

"""
    Contains problem-specific logic for reading the input and writing the output
"""

# Problem-specific ID
PROBLEM_ID = '6417837228818432'

# List of problem-specific input filenames, and associated dataset ID
INPUT_FILENAMES = {
    'a_example.txt': '6199627120377856',
    'b_lovely_landscapes.txt': '5239399268745216',
    'c_memorable_moments.txt': '5185683152961536',
    'd_pet_pictures.txt': '6378347655331840',
    'e_shiny_selfies.txt': '4834468208574464',
}

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
        N = map(int, next(f).split())

        def parse_line(line):
            l = line.split()
            h = 0 if l[0] == 'H' else 1
            n = int(l[1])
            return [h, l[2:]]

        photos = [parse_line(line) for line in f]
        return (N, photos)

def evaluate(input_data, output_data):
    """
        Example output evaluation for the 'Pizza' problem.
     """
    N, lines = input_data

    # Validate that all slices are valid
    valid = True
    score = 0
    for rect in output_data:
        r1, c1, r2, c2 = rect
        slice = lines[r1:r2+1, c1:c2+1]
        slice_tomato_count = slice.sum()
        slice_mushroom_count = slice.size - slice_tomato_count
        if slice.size > H:
            valid = False
            print("ERROR: Slice too big - {} is more than {} - ({}, {}, {}, {}): {}".format(slice.size, H, r1, c1, r2, c2, slice))
        elif slice_tomato_count < L:
            valid = False
            print("ERROR: Slice without enough tomato - {} is less than {} - ({}, {}, {}, {}): {}".format(slice_tomato_count, L, r1, c1, r2, c2, slice))
        elif slice_mushroom_count < L:
            valid = False
            print("ERROR: Slice without enough mushrooms - {} is less than {} - ({}, {}, {}, {}): {}".format(slice_mushroom_count, L, r1, c1, r2, c2, slice))
        else:
            score += slice.size

    # Score is the sum of all cells in all slices
    if valid:
        score = sum([(abs(r[0] - r[2]) + 1) * (abs(r[1] - r[3]) + 1) for r in output_data])

    return valid, score

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
            f.write(' '.join(slide) + '\n')
