from pathlib import Path
import os

import zipfile
import json

import pandas as pd
import awswrangler as wr


# CONSTANTS
ROOT_PATH = os.getcwd()
RAW_PATH = Path(f"{ROOT_PATH}/data/raw")
TRUSTED_PATH = Path(f"{ROOT_PATH}/data/trusted")
S3_RAW_DATA = 's3://data-lake-protein/raw/dados.zip'
S3_TRUSTED_URI = 's3://data-lake-protein/trusted'
COLUMN_MAP_PATH = Path(f"{ROOT_PATH}/src/data_pipeline/column_map")


# MAKE RAW TO TRSUTED PROCESS
class TrustedProcess():

    def __init__(self,
                 s3_raw_path, raw_folder, raw_data_file, 
                 quality_folder, quality_file, 
                 s3_trusted_path, trusted_folder, trusted_data_file):
        
        self.s3_raw_path = s3_raw_path
        self.raw_folder = raw_folder
        self.raw_data_file = raw_data_file
        self.quality_folder = quality_folder
        self.quality_file = quality_file
        self.s3_trusted_path = s3_trusted_path
        self.trusted_folder = trusted_folder
        self.trusted_data_file = trusted_data_file
    
    def download_s3_file(self):
        return wr.s3.download(path=self.s3_raw_path, local_file=os.path.join(self.raw_folder, 'dados.zip'))

    def unzip_file(self):
        raw_folder = self.raw_folder
        zip_file = os.path.join(raw_folder, 'dados.zip')
        z = zipfile.ZipFile(zip_file)
        return z.extractall(raw_folder) 

    def read_csv_files(self):
        csv_path = os.path.join(self.raw_folder, self.raw_data_file)
        df = pd.read_csv(csv_path)
        return df

    def open_quality_artifact(self):
        path_json = os.path.join(self.quality_folder, self.quality_file)    
        with open(path_json) as f:
            json_quality = json.load(f)
        return json_quality

    def quality(self, df: pd.DataFrame, key_dict: dict):
        df_quality = pd.DataFrame()
        for column in key_dict:
            column_type = key_dict[column]
            column_name = f"{column.upper()}_{column_type.upper()}"
            df_quality[column_name] = df[column].dropna().astype(column_type)
        return df_quality

    def save_parquet(self, df: pd.DataFrame):
        path_save = os.path.join(self.trusted_folder, self.trusted_data_file)
        df.to_parquet(path_save, index=False)
        return wr.s3.upload(local_file=path_save, path=f'{self.s3_trusted_path}/{self.trusted_data_file}')
    
    def run(self):
        self.download_s3_file()
        self.unzip_file()
        df = self.read_csv_files()
        json_quality = self.open_quality_artifact()
        df_quality = self.quality(df, json_quality)
        return self.save_parquet(df_quality)


# MAIN PROCESS
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

# RUN
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