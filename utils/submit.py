import requests
import urllib.parse

from utils import common

def get_headers():
    try:
        with open(common.TOKEN_FILE, 'r') as f:
            return {
                'Authorization': 'Bearer {}'.format(f.read().replace('\n', ''))
            }
    except FileNotFoundError:
        raise Exception('ERROR: Token file is missing: "{}"'.format(common.TOKEN_FILE))

def get_upload_url():
    try :
        response = requests.get('https://hashcode-judge.appspot.com/api/judge/v1/upload/createUrl', headers=get_headers())
        response.raise_for_status()
        return response.json()['value'] # Return upload URL
    except KeyError:
        raise Exception('ERROR: Failed to get upload url - received: {}'.format(response.json()))
    except requests.HTTPError:
        raise Exception('ERROR: Failed to get upload url - received: {}'.format(response.text))

def upload_file(filename):
    try:
        upload_url = get_upload_url()
        response = requests.post(upload_url, files={'file': open(filename, 'rb')})
        response.raise_for_status()
        return response.json()['file'][0] # Return blob reference to uploaded file
    except KeyError:
        raise Exception('ERROR: Failed to upload file - received: {}'.format(response.json()))
    except requests.HTTPError:
        raise Exception('ERROR: Failed to upload file - received: {}'.format(response.text))

def submit_file(dataset_id, solution_filename, source_filename):
    """
        To submit a solution, one must upload both source code and solution beforehand.
        For each file (`upload_file()`), a new upload url is fetched with `get_upload_url()`,
        after which the file can be uploaded.
    """
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
    return response['id'] # Return submission ID

def get_scores(submissions):
    response = requests.get('https://hashcode-judge.appspot.com/api/judge/v1/submissions/5720363694555136', headers=get_headers()).json()
    for item in response['items']:
        if item['id'] in submissions.values():
            if not item['scored']:
                print('Solution for "{}" still not scored'.format(item['dataSet']['name']))
            else:
                if item['valid']:
                    print('Solution for "{}" got {}{}'.format(item['dataSet']['name'], item['score'], ' - new record!' if item['best'] else ''))
                else:
                    print('Solution for "{}" not valid: {}'.format(item['dataSet']['name'], item['errorMessage']))

            print('')
