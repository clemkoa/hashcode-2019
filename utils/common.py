import glob
import os
import numpy as np
import time
import zipfile

from utils import processing
from utils import submit

### Constants ###
INPUT_FOLDER = 'input'
OUTPUT_FOLDER = 'output'

TOKEN_FILE = 'token.txt'
SOURCE_CODE_FILENAME = '{}/source.zip'.format(OUTPUT_FOLDER)
# Mapping of input filename to dataset ID
INPUT_FILENAMES = {
    'a_example.in': '6140197687263232',
    'b_small.in': '6571563717492736',
    'c_medium.in': '5024167346831360',
    'd_big.in': '6561530623557632'
}

def pretty_print_time(t):
    min = int(t / 60)
    sec = t % 60

    return ('{}min '.format(min) if min > 0 else '') \
        + '{:.2f}s'.format(sec)

# Will zip all Python files and put the resulting archive in the OUTPUT_FOLDER
def zip_code():
    zipf = zipfile.ZipFile(SOURCE_CODE_FILENAME, 'w', zipfile.ZIP_DEFLATED)
    for source_file in glob.glob('*.py') + glob.glob('**/*.py'):
        zipf.write(source_file)
    zipf.close()

def run_solution(func):
    zip_code()

    results = {}
    for f in INPUT_FILENAMES:
        print('{:#^30}'.format(f))

        input_filename = os.path.join(INPUT_FOLDER, f)
        output_filename = os.path.join(OUTPUT_FOLDER, f)
        if not os.path.exists(input_filename):
            print('WARN: Missing input file "{}", skipping'.format(input_filename))
        else:
            input_data = processing.read_input(input_filename)
            print('Computing solution...')
            start_time = time.time()

            output_data = func(input_data)

            elapsed = time.time() - start_time
            processing.write_output(output_filename, output_data)
            submission_id = submit.submit_file(INPUT_FILENAMES[f], output_filename, SOURCE_CODE_FILENAME)

            # TODO: Plug in evaluation function
            score = 0

            results[f] = {
                'submission_id': submission_id,
                'internal_score': score,
                'elapsed': elapsed
            }

            print('Took {} and scored {}'.format(pretty_print_time(elapsed), score))
        print('{:#^30}'.format(''))
        print('')

    print(results)
