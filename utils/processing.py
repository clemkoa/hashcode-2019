import os
import numpy as np

"""
    Contains problem-specific logic for reading the input and writing the output
"""

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
            return [0 if c is 'M' else 1 for c in line]

        lines = np.array([parse_line(line) for line in f])
        return (R, C, L, H, lines)

def write_output(filename, input_data):
    """
        Example output writer for the 'Pizza' problem
        Input data is a list of slices, where each slice is a list of 4 elements:
        (starting row, starting column, ending row, ending column)
    """
    folder = os.path.dirname(filename)
    if not os.path.exists(folder):
        os.mkdir(folder)

    with open(filename, 'w') as f:
        f.write(str(len(input_data)) + '\n')
        for rect in input_data:
            print(rect)
            f.write(' '.join(map(str, rect)) + '\n')
