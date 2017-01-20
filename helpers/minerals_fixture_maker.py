"""
Creates a fixture file with the correct field names from the minerals.json
file content supplied in 'assets'. The fixtures file is used to populate the
database via manage.py loaddata, should be run from the root directory for the project
"""

import json
import os

if __name__ == '__main__':
    file_loc = os.path.join(os.getcwd(), 'assets/json/minerals.json')
    file_save = os.path.join(os.getcwd(), 'minerals/fixtures/minerals_dump.json')

    with open(file_loc, encoding='utf8', mode='r') as file_r:
        data = json.load(file_r)

    fixture = []
    for location, mineral in enumerate(data):
        new_mineral = {}
        for key, value in mineral.items():
            if len(key) > 1:
                new_key = '_'.join(key.split(' '))
                new_mineral.update({new_key: value})
            else:
                new_mineral.update({key: value})
        entry = {
            "model": "minerals.mineral",
            "pk": location + 1,
            "fields":
                new_mineral
        }
        fixture.append(entry)

    with open(file_save, encoding='utf8', mode='w') as file_s:
        json.dump(obj=fixture, indent=4, fp=file_s)