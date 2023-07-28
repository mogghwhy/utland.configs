import json

def read_data(file_name):
    with open(file_name,'r') as json_file:
        json_data = json.load(json_file)
    return json_data

def write_data(items, file_name):
    data = {}
    data['items'] = items
    json_data = json.dumps(data)
    with open(file_name, 'w') as json_file:
        json_file.write(json_data)
