import os
import numpy as np

"""
    Contains problem-specific logic for reading the input and writing the output
"""

# Problem-specific ID
PROBLEM_ID = '5720363694555136'

# List of problem-specific input filenames, and associated dataset ID
INPUT_FILENAMES = {
    'a_example.in': '6140197687263232',
    'b_small.in': '6571563717492736',
    'c_medium.in': '5024167346831360',
    'd_big.in': '6561530623557632'
}

def read_input(filename):
    """
        Example input reader for the 'Pizza' problem.
        Returns a tuple of:
            R:      Number of rows in the input
            C:      Number of columns in the input
            L:      Minimum number of each ingredient in a slice
            H:      Maximum number of cells in a slice
            lines:  np.array of the input, where mushrooms are zeros and tomatoes ones
    """
    with open(filename, 'r') as f:
        R, C, L, H = map(int, next(f).split())

        def parse_line(line):
            line = line.replace('\n', '')
            return [0 if c is 'M' else 1 for c in line]

        lines = np.array([parse_line(line) for line in f])
        return (R, C, L, H, lines)

def evaluate(input_data, output_data):
    """
        Example output evaluation for the 'Pizza' problem.
     """
    R, C, L, H, lines = input_data

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
        Example output writer for the 'Pizza' problem.
        Input data is a list of slices, where each slice is a list of 4 elements:
        (starting row, starting column, ending row, ending column)
    """
    folder = os.path.dirname(filename)
    if not os.path.exists(folder):
        os.mkdir(folder)

    with open(filename, 'w') as f:
        f.write(str(len(output_data)) + '\n')
        for rect in output_data:
            f.write(' '.join(map(str, rect)) + '\n')
