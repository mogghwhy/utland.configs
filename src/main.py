import json
from sys import argv
from skraper import scrape
from stagedata import read_config_data
from stagedata import read_meta_data
from stagedata import write_data
from stagedata import StageDataUtils

start_index = None
if len(argv) == 6:
    meta_data = argv[1]
    meta_data_format = argv[2]
    config_data = argv[3]
    output_data = argv[4]
    output_format = argv[5]
elif len(argv) == 7:
    meta_data = argv[1]
    meta_data_format = argv[2]
    config_data = argv[3]
    output_data = argv[4]
    output_format = argv[5]
    start_index = int(argv[6])
else:
    print("This script needs exactly 5 or 6 arguments, aborting")
    exit()

stage_data_utils = StageDataUtils(meta_data, meta_data_format, config_data, output_data, output_format)
meta_data_json = stage_data_utils.read_meta_data()
config_json = stage_data_utils.read_config(config_data)

if start_index is not None:
    data = scrape(meta_data_json, config_json, stage_data_utils.write_data, start_index)
else:
    data = scrape(meta_data_json, config_json, stage_data_utils.write_data)

