import os
import zipfile
import json
import pandas as pd
import awswrangler as wr


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
        return wr.s3.download(path=self.s3_raw_path, local_file=os.path.join(self.raw_folder, 'protein-data-set.zip'))

    def unzip_file(self):
        raw_folder = self.raw_folder
        zip_file = os.path.join(raw_folder, 'protein-data-set.zip')
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
