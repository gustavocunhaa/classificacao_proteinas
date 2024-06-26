import os
from pathlib import Path

from data_pipeline.trusted import TrustedProcess
from data_pipeline.refined import RefinedProcess


# CONSTANTS
ROOT_PATH = os.getcwd()

RAW_PATH = Path(f"{ROOT_PATH}/data/raw")
S3_RAW_DATA = 's3://data-lake-protein/raw/dados.zip'
S3_TRUSTED_URI = 's3://data-lake-protein/trusted'
COLUMN_MAP_PATH = Path(f"{ROOT_PATH}/src/data_pipeline/column_map")

TRUSTED_PATH = Path(f"{ROOT_PATH}/data/trusted")
S3_TRUSTED_URI = 's3://data-lake-protein/trusted'

REFINED_PATH = Path(f"{ROOT_PATH}/data/refined")
S3_REFINED_URI = 's3://data-lake-protein/refined'


# CONFIGS
config_dict = {
    'structure': {
        'raw_csv_file': 'pdb_data_no_dups.csv',
        'quality_json_file' : 'data_structure.json',
        'trusted_parquet_file': 'data_structure.parquet' 
    },
    'sequence': {
        'raw_csv_file': 'pdb_data_seq.csv',
        'quality_json_file' : 'data_sequence.json',
        'trusted_parquet_file': 'data_sequence.parquet' 
    }
}

# MAIN PROCESS
for file_config in config_dict:
    TrustedProcess(
        s3_raw_path=S3_RAW_DATA,
        raw_folder=RAW_PATH,           
        raw_data_file=config_dict[file_config]['raw_csv_file'],
        quality_folder=COLUMN_MAP_PATH,
        quality_file=config_dict[file_config]['quality_json_file'],
        s3_trusted_path=S3_TRUSTED_URI,
        trusted_folder=TRUSTED_PATH,
        trusted_data_file=config_dict[file_config]['trusted_parquet_file']
    ).run()

RefinedProcess(
    s3_trusted_path=S3_TRUSTED_URI,
    trusted_folder=TRUSTED_PATH,
    trusted_data_files=['data_sequence.parquet', 'data_structure.parquet'],
    s3_refined_path=S3_REFINED_URI,
    refined_folder=REFINED_PATH,
).run()