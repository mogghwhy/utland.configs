# utland
## Utland is a multi-stage data scraper that extracts information about shows, movies, and programs available on the NRK website (https://tv.nrk.no/programmer/utland).

## initial setup
git clone https://github.com/mogghwhy/utland  
python -m venv ~/utenv  
source ~/utenv/bin/activate  
cd ./utland  
python -m pip install -r requirements.txt  
cd ./src

## how to run the script
python main.py metadata_stateNN.format "format" config_stageNN.json metadata_stageNN++.format "format"

## running stage 00
python main.py metadata_stage00.json "json" config_stage00.json metadata_stage01.csv "csv"

## running stage 01
python main.py metadata_stage01.json "json" config_stage01.json metadata_stage02.csv "csv"

## running stage 02
python main.py metadata_stage02.json "json" config_stage02.json metadata_stage03.csv "csv"