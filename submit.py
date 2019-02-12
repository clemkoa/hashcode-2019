import requests
import urllib.parse

SOURCE_INPUT = 'output/source.zip'
SOLUTION_INPUTS = {
    '6140197687263232': 'output/a_example.in',
    '6571563717492736': 'output/b_small.in',
    '5024167346831360': 'output/c_medium.in',
    '6561530623557632': 'output/d_big.in'
}

def get_headers():
    with open('token.txt', 'r') as f:
        return {
            'Authorization': 'Bearer {}'.format(f.read().replace('\n', ''))
        }

def get_upload_url():
    response = requests.get('https://hashcode-judge.appspot.com/api/judge/v1/upload/createUrl', headers=get_headers()).json()
    return response['value'] # Return upload URL

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
    for dataset_id in SOLUTION_INPUTS:
        submit_file(dataset_id, SOLUTION_INPUTS[dataset_id], SOURCE_INPUT)

if __name__ == '__main__':
    submit()
