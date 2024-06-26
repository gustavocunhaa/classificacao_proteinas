from pathlib import Path
import os
import json

import pandas as pd
import awswrangler as wr

# CONSTANTS
ROOT_PATH = os.getcwd()
TRUSTED_PATH = Path(f"{ROOT_PATH}/data/trusted")
REFINED_PATH = Path(f"{ROOT_PATH}/data/refined")
S3_TRUSTED_URI = 's3://data-lake-protein/trusted'
S3_REFINED_URI = 's3://data-lake-protein/refined'
TABLE_CONFIG_PATH = Path(f"{ROOT_PATH}/src/data_pipeline/tables/tables_config.json")


# MAKE TRSUTED TO REFINED PROCESS
class RefinedProcess():

    def __init__(self,  
                 s3_trusted_path, trusted_folder, trusted_data_files,
                 s3_refined_path, refined_folder):
        
        self.s3_trusted_path = s3_trusted_path
        self.trusted_folder = trusted_folder
        self.trusted_data_files = trusted_data_files
        self.s3_refined_path = s3_refined_path
        self.refined_folder = refined_folder
    
    def download_s3_files(self, file_name):
        local = os.path.join(self.trusted_folder, file_name)
        return wr.s3.download(path=f"{self.s3_trusted_path}/{file_name}", local_file=local)

    def read_parquet_file(self, file_name):
        parquet_path = os.path.join(self.trusted_folder, file_name)
        df = pd.read_parquet(parquet_path)
        return df
    
    def create_refined_table(self, df: pd.DataFrame, columns: list, id_name='STRUCTUREID_STR', id_single="False"):
        df = df[columns] 
        df = df.dropna() 
        if id_single == "True":
            df.drop_duplicates(subset=id_name)
        colunas_str = [col for col in df.columns if col.endswith('STR')]
        df[colunas_str] = df[colunas_str].apply(lambda x: x.str.upper())
        return df
    
    def save_parquet(self, df: pd.DataFrame, file_name):
        file = f"{file_name}.parquet"
        path_save = os.path.join(self.refined_folder, file)
        df.to_parquet(path_save, index=False)
        return wr.s3.upload(local_file=path_save, path=f'{self.s3_refined_path}/{file}')
    
    def run(self):
        for file in self.trusted_data_files:
            self.download_s3_files(file)

        with open(TABLE_CONFIG_PATH) as j:
            config_table = json.load(j)

        for table in config_table:
            df_origen  = self.read_parquet_file(config_table[table]['origen_file'])
            df_refined = self.create_refined_table(df=df_origen,
                                                   columns=config_table[table]['columns_selected'],
                                                   id_single=config_table[table]['id_single'] 
                                                   )
            self.save_parquet(df=df_refined, file_name=table) 

# MAIN PROCESS
# RUN
RefinedProcess(
    s3_trusted_path=S3_TRUSTED_URI,
    trusted_folder=TRUSTED_PATH,
    trusted_data_files=['data_sequence.parquet', 'data_structure.parquet'],
    s3_refined_path=S3_REFINED_URI,
    refined_folder=REFINED_PATH,
).run()