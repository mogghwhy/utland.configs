import json
from sys import argv
from skraper import scrape
from stagedata import read_config_data
from stagedata import read_meta_data
from stagedata import write_data
from stagedata import StageDataUtils


if len(argv) == 4:
    meta_data = argv[1]
    config_data = argv[2]
    output_data = argv[3]
else:
    print("This script needs exactly three arguments, aborting")
    exit()

stage_data_utils = StageDataUtils(meta_data, 'json', config_data, output_data, 'csv')
meta_data_json = stage_data_utils.read_meta_data()
# meta_data_json = read_meta_data(meta_data)
# print(meta_data_json)
config_json = read_config_data(config_data)
# config_json2 = stage_data_utils.read_config(config_data)
# print(config_json2)
data = scrape(meta_data_json, config_json, stage_data_utils.write_data)
#write_data(data, output_data)

