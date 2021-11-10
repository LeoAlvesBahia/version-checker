import requests
import json
from LibClass import LibClass

with open('requirements.txt', 'r') as file:
    # splitlines remove \n and list comprehension to remove empty values
    file_as_string = [a for a in file.read().splitlines() if a != '']

data = []
for item in file_as_string:
    lib = LibClass(item)
    lib = lib.separate_values()

    response = requests.get(
        url=f'https://pypi.python.org/pypi/{lib.name}/json'
    )
    response = json.loads(response.text)

    data.append({
        'packageName': response['info']['name'],
        'currentVersion': lib.version if lib.version else response['info']['version'],
        'latestVersion': response['info']['version'],
        'outOfDate': lib.check_version(response['info']['version'])
    })

print(json.dumps(data, indent=4))
