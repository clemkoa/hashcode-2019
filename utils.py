import glob
import os
import numpy as np
import zipfile

### Constants ###
INPUT_FOLDER = 'input'
OUTPUT_FOLDER = 'output'

TOKEN_FILE = 'token.txt'
SOURCE_INPUT = '{}/source.zip'.format(OUTPUT_FOLDER)
SOLUTION_INPUTS = {
    '6140197687263232': '{}/a_example.in'.format(OUTPUT_FOLDER),
    '6571563717492736': '{}/b_small.in'.format(OUTPUT_FOLDER),
    '5024167346831360': '{}/c_medium.in'.format(OUTPUT_FOLDER),
    '6561530623557632': '{}/d_big.in'.format(OUTPUT_FOLDER)
}

# Will zip all Python files and put the resulting archive in the OUTPUT_FOLDER
def zip_code():
    zipf = zipfile.ZipFile(os.path.join(OUTPUT_FOLDER, 'source.zip'), 'w', zipfile.ZIP_DEFLATED)
    for source_file in glob.glob('**.py'):
        zipf.write(source_file)
    zipf.close()
