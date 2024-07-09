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
        path_s3 = self.s3_raw_path
        print(f">>> Download s3 file {path_s3}")
        
        try:
            wr.s3.download(path=path_s3, local_file=os.path.join(self.raw_folder, 'protein-data-set.zip'))
            print(f"SUCESS: Download s3 file")
        except ValueError as e:
            print(f"EROR: Download s3 file - {e}")

    def unzip_file(self):
        raw_folder = self.raw_folder
        zip_file = os.path.join(raw_folder, 'protein-data-set.zip')
        print(f">>> Unzipe {zip_file} file")
        
        try:
            z = zipfile.ZipFile(zip_file)
            z.extractall(raw_folder)
            print(f"SUCESS: Unzipe file")
        except ValueError as e:
            print(f"ERROR: Unzipe file - {e}") 

    def read_csv_files(self):
        csv_path = os.path.join(self.raw_folder, self.raw_data_file)
        print(f">>> Reading csv {csv_path} file")
        
        try: 
            df = pd.read_csv(csv_path)
            print("SUCESS: csv read to Dataframe")
        except ValueError as e:
            print(f"ERROR: csv read to Dataframe - {e}")
        
        return df

    def open_quality_artifact(self):
        map_file = self.quality_file
        path_json = os.path.join(self.quality_folder, map_file)    
        print(f">>> Open quality {map_file} map")
        try:
            with open(path_json) as f:
                json_quality = json.load(f)
            print(f"SUCESS: Quality map")
        except ValueError as e:
            print(f"ERROR: Quality map - {e}")
        
        return json_quality

    def quality(self, df: pd.DataFrame, key_dict: dict):
        print(f">>> Data quality process")
        
        try:
            df_quality = pd.DataFrame()
            for column in key_dict:
                column_type = key_dict[column]
                column_name = f"{column.upper()}_{column_type.upper()}"
                df_quality[column_name] = df[column].dropna().astype(column_type)
            print(f"SUCESS: Quality process")
        except ValueError as e:
            print(f"ERRO: Quality process - {e}")

        return df_quality

    def save_parquet(self, df: pd.DataFrame):
        trusted_data_file = self.trusted_data_file
        path_save = os.path.join(self.trusted_folder, trusted_data_file)
        s3_trusted_path = self.s3_trusted_path
        print(f">>> Save parquet {trusted_data_file} trusted file on s3_trusted_path")
        
        try:
            df.to_parquet(path_save, index=False)
            wr.s3.upload(local_file=path_save, path=f'{s3_trusted_path}/{trusted_data_file}')
            print(f"SUCESS: Trusted file save")
        except ValueError as e:
            print(f"ERROR: Trusted file save - {e}")

    def run(self):
        print(f"# START TRUSTED METHOD")
        self.download_s3_file()
        self.unzip_file()
        df = self.read_csv_files()
        json_quality = self.open_quality_artifact()
        df_quality = self.quality(df, json_quality)
        self.save_parquet(df_quality)
        print(f"# FINISH TRUSTED METHOD")