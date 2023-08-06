import json
from sys import argv
from skraper import scrape
from stagedata import read_config_data
from stagedata import read_meta_data
from stagedata import write_data
from stagedata import StageDataUtils

start_index = None
if len(argv) == 4:
    meta_data = argv[1]
    config_data = argv[2]
    output_data = argv[3]
elif len(argv) == 5:
    meta_data = argv[1]
    config_data = argv[2]
    output_data = argv[3]
    start_index = int(argv[4])
else:
    print("This script needs exactly three arguments, aborting")
    exit()

stage_data_utils = StageDataUtils(meta_data, 'json', config_data, output_data, 'csv')
meta_data_json = stage_data_utils.read_meta_data()
config_json = stage_data_utils.read_config(config_data)

if start_index is not None:
    data = scrape(meta_data_json, config_json, stage_data_utils.write_data, start_index)
else:
    data = scrape(meta_data_json, config_json, stage_data_utils.write_data)

