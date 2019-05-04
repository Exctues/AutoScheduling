import requests
import json


def run_gscript(json_path, update=False, url=''):
    with open(json_path, "r", encoding="utf-8") as input_file:
        data_list = json.load(input_file)
    data = {
        'method': 'POST',
        "Accept": "application/json",
        'contentType': 'application/json',
        'update': update,
        'payload': json.dumps(data_list)}

    if update:
        data['update'] = 1
        data['url'] = url
    else:
        data['update'] = 0

    r = requests.post(
        url='https://script.google.com/macros/s/AKfycbzVirV31VN843VvmkpjX6IYv2sbVqF1CG4c8Jw8m9II7gHO5vM/exec',
        data=data)
    # print(r.text)
    return r.text

# run_gscript('../schedule/json/test.json')
