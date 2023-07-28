import json
from sys import argv
from skraper import scrape
from stagedata import read_config_data
from stagedata import read_meta_data
from stagedata import write_data


if len(argv) == 4:
    meta_data = argv[1]
    config_data = argv[2]
    output_data = argv[3]
else:
    print("This script needs exactly three arguments, aborting")
    exit()

meta_data_json = read_meta_data(meta_data)
config_json = read_config_data(config_data)
data = scrape(meta_data_json, config_json)
write_data(data, output_data)

