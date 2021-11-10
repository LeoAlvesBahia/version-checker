import base64
import requests
import json
from LibClass import LibClass

# info to github file
username = 'esdras-tavares'
reponame = 'test_python'
path = 'requirements.txt'
url = f'https://api.github.com/repos/{username}/{reponame}/contents/{path}'

response = requests.get(
    url=url
)
if response.status_code == requests.codes.ok:
    response = response.json()
    # file from github come encoded base64. we decode from base64 and 
    # convert from bytes to string with .decode()
    file_as_string = base64.b64decode(response['content']).decode()


# splitlines remove \n and list comprehension to remove empty values
file_as_string = [a for a in file_as_string.splitlines() if a != '']


data = []
for item in file_as_string:
    lib = LibClass(item)
    lib = lib.separate_values()

    response = requests.get(
        url=f'https://pypi.python.org/pypi/{lib.name}/json'
    )
    if response.status_code == requests.codes.ok:
        response = json.loads(response.text)

        data.append({
            'packageName': response['info']['name'],
            'currentVersion': lib.version if lib.version else response['info']['version'],
            'latestVersion': response['info']['version'],
            'outOfDate': lib.check_version(response['info']['version'])
        })
    else:
        print(f'lib {lib.name} not found on PyPI.')

print(json.dumps(data, indent=4))
