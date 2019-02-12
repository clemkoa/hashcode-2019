import os
import numpy as np
import zipfile

def zip_code(OUTPUT_FOLDER):
    zipf = zipfile.ZipFile(os.path.join(OUTPUT_FOLDER, 'source.zip'), 'w', zipfile.ZIP_DEFLATED)
    zipf.write('main.py')
    zipf.close()

def read(INPUT_FOLDER, file_name):
    path = os.path.join('input', file_name)
    with open(path, 'r') as f:
        R, C, L, H = map(int, next(f).split())

        def parse_line(line):
            return [0 if c is 'M' else 1 for c in line]

        lines = np.array([parse_line(line) for line in f])
        return R, C, L, H, lines

def write(path, solution):
    folder = os.path.dirname(path)
    if not os.path.exists(folder):
        os.mkdir(folder)

    with open(path, 'w') as f:
        f.write(str(len(solution)) + '\n')
        for rect in solution:
            f.write(' '.join(map(str, rect)) + '\n')

if __name__ == '__main__':
    INPUT_FOLDER = 'input'
    OUTPUT_FOLDER = 'output'
    zip_code(OUTPUT_FOLDER)
    files = os.listdir(INPUT_FOLDER)
    for file in files:
        R, C, L, H, lines = read(INPUT_FOLDER, file)
        write(os.path.join(OUTPUT_FOLDER, file), [[0, 0, 0, H-1]])
