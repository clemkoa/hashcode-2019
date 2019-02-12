import os
import requests
import urllib.parse

import utils

def get_headers():
    with open(utils.TOKEN_FILE, 'r') as f:
        return {
            'Authorization': 'Bearer {}'.format(f.read().replace('\n', ''))
        }

def get_upload_url():
    try :
        response = requests.get('https://hashcode-judge.appspot.com/api/judge/v1/upload/createUrl', headers=get_headers()).json()
        return response['value'] # Return upload URL
    except KeyError:
        raise Exception('Failed to get upload url - received: {}'.format(response))

def upload_file(filename):
    upload_url = get_upload_url()
    response = requests.post(upload_url, files={'file': open(filename, 'rb')}).json()
    return response['file'][0] # Return blob reference to uploaded file

def submit_file(dataset_id, solution_filename, source_filename):
    solution_blob = upload_file(solution_filename)
    source_blob = upload_file(source_filename)

    submit_url = 'https://hashcode-judge.appspot.com/api/judge/v1/submissions?{}'.format(
        urllib.parse.urlencode({
            'dataSet': dataset_id,
            'submissionBlobKey': solution_blob,
            'sourcesBlobKey': source_blob
        })
    )
    response = requests.post(submit_url, headers=get_headers()).json()
    print('Submitted solution for "{}"'.format(response['dataSet']['name']))

def submit():
    # Checks
    if not os.path.exists(utils.TOKEN_FILE):
        raise Exception('Token file is missing: "{}"'.format(utils.TOKEN_FILE))
    if not os.path.exists(utils.SOURCE_INPUT):
        raise Exception('Source code is missing: "{}"'.format(utils.SOURCE_INPUT))

    for dataset_id in utils.SOLUTION_INPUTS:
        if os.path.exists(utils.SOLUTION_INPUTS[dataset_id]):
            submit_file(dataset_id, utils.SOLUTION_INPUTS[dataset_id], utils.SOURCE_INPUT)
        else:
            print('Skipping missing input: "{}"'.format(utils.SOLUTION_INPUTS[dataset_id]))

if __name__ == '__main__':
    submit()
