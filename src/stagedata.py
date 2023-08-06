import os
import csv
import json

class StageDataUtils:
    def __init__(self, input_file, input_format, config_file, output_file, output_format):
        self.output_file = output_file
        self.input_file = input_file
        self.config_file = config_file
        self.write_data = self._get_output_writer(output_format)
        self.read_data = self._get_input_reader(input_format)
        self.read_config = self._read_from_json

    def _get_input_reader(self, format):
        if format == 'json':
            return self._read_from_json
        elif format == 'csv':
            return self._read_from_csv
        else:
            raise ValueError(format)

    def _get_output_writer(self, format):
        if format == 'json':
            return self._write_to_json
        elif format == 'csv':
            return self._write_to_csv
        else:
            raise ValueError(format)

    def _write_to_csv(self, item):
        field_names = []
        if isinstance(item, list):
            for it in item:
                field_names += list(it.keys())
                field_names = list(set(field_names))
        else:
            field_names = list(set(item.keys()))
        field_names.sort()
        if os.path.exists(self.output_file):
            with open(self.output_file, 'a', encoding='utf-8', newline='\n') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=field_names, dialect='unix')
                if isinstance(item, list):
                    for it in item:
                        writer.writerow(it)
                else:
                    writer.writerow(item)
        else:
            with open(self.output_file, 'w', encoding='utf-8', newline='\n') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=field_names, dialect='unix')
                writer.writeheader()
                if isinstance(item, list):
                    for it in item:
                        writer.writerow(it)
                else:
                    writer.writerow(item)

    def _write_to_json(self, items):
        if os.path.exists(self.output_file):            
            with open(self.output_file, 'r+', encoding='utf-8') as json_file:
                json_data = json.load(json_file)
                json_data['items'] += (items)
                json_file.seek(0)
                json.dump(json_data, json_file, ensure_ascii=True, indent = 4)
        else:
            with open(self.output_file, 'w+', encoding='utf-8') as json_file:
                empty = {}
                empty['items'] = []
                empty['items'] += items
                json.dump(empty, json_file, ensure_ascii=True, indent = 4)                

    def _read_from_csv(self, file):
        with open(self.input_file,'r', newline='\n', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            items = {}
            items['items'] = []
            items['items'] += list(reader)
            return items

    def _read_from_json(self, file):
        with open(file, 'r', encoding='utf-8') as json_file:
            json_data = json.load(json_file)            
        return json_data
    
    def read_meta_data(self):        
        return self.read_data(self.input_file)['items']




def read_config_data(file_name):
    return read_data(file_name)

def read_meta_data(file_name):    
    return read_data(file_name)['items']

def read_data(file_name):
    with open(file_name,'r', encoding='utf-8') as json_file:
        json_data = json.load(json_file)
    return json_data

def write_data(items, file_name):
    data = {}
    data['items'] = items
    json_data = json.dumps(data, ensure_ascii=True, indent=4)
    with open(file_name, 'w', encoding='utf-8') as json_file:
        json_file.write(json_data)