import glob
import os
import numpy as np
import time
import zipfile

from utils import processing
from utils import submit

"""
    Problem agnostic functions for running the solution and submitting it.
"""

### Constants ###
INPUT_FOLDER = 'input'
OUTPUT_FOLDER = 'output'

TOKEN_FILE = 'token.txt'
SOURCE_CODE_FILENAME = '{}/source.zip'.format(OUTPUT_FOLDER)

def pretty_print_time(t):
    """
        Returns a pretty string for showing elapsed time.
    """

    min = int(t / 60)
    sec = t % 60

    return ('{}min '.format(min) if min > 0 else '') \
        + '{:.2f}s'.format(sec)

def zip_code():
    """
        Zips all Python files at the root level and subfolders for submission.
    """

    zipf = zipfile.ZipFile(SOURCE_CODE_FILENAME, 'w', zipfile.ZIP_DEFLATED)
    for source_file in glob.glob('*.py') + glob.glob('**/*.py'):
        zipf.write(source_file)
    zipf.close()

def run_solution(func, local_only=False):
    """
        Runs the given `func` on each available problem input.
        Use `local_only=True` to not submit to the Judge System.
    """

    zip_code()

    results = {}
    for f in processing.INPUT_FILENAMES:
        print('{:#^30}'.format(f))

        input_filename = os.path.join(INPUT_FOLDER, f)
        dataset_id = processing.INPUT_FILENAMES[f]
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

            submission_id = None
            if not local_only:
                submission_id = submit.submit_file(dataset_id, output_filename, SOURCE_CODE_FILENAME)

            # TODO: Plug in local evaluation function
            score = 0

            results[f] = {
                'submission_id': submission_id,
                'internal_score': score,
                'elapsed': elapsed
            }

            print('Took {} and scored {}'.format(pretty_print_time(elapsed), score))
        print('{:#^30}'.format(''))
        print('')

    # TODO: Plug in submit.get_scores()

    # TODO: Print results
    print(results)
