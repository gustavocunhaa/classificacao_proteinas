from pathlib import Path
import os
import json
import pandas as pd
import awswrangler as wr


# MAKE TRSUTED TO REFINED PROCESS
class RefinedProcess():

    def __init__(self,  
                 s3_trusted_path, trusted_folder, trusted_data_files,
                 config_file_path, s3_refined_path, refined_folder):
        
        self.s3_trusted_path = s3_trusted_path
        self.trusted_folder = trusted_folder
        self.trusted_data_files = trusted_data_files
        self.config_file_path = config_file_path 
        self.s3_refined_path = s3_refined_path
        self.refined_folder = refined_folder
    
    def download_s3_files(self, file_name):
        local = os.path.join(self.trusted_folder, file_name)
        s3_trusted_path = self.s3_trusted_path
        print(f">>> Download {file_name} for {s3_trusted_path}")
        
        try:
            wr.s3.download(path=f"{s3_trusted_path}/{file_name}", local_file=local)
            print(f"SUCESS: Download file")
        except ValueError as e:
            print(f"ERROR: Download file - {e}")

    def read_parquet_file(self, file_name):
        parquet_path = os.path.join(self.trusted_folder, file_name)
        print(f">>> Read {file_name} parquet file")
        
        try:
            df = pd.read_parquet(parquet_path)
            print(f"SUCESS: Reading parquet file")
        except ValueError as e:
            print(f"ERROR: Reading parquet file - {e}")
        
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
        s3_path = self.s3_refined_path
        print(f">>> Saving {file_name} parquet file on {s3_path}")

        try:
            df.to_parquet(path_save, index=False)
            wr.s3.upload(local_file=path_save, path=f'{s3_path}/{file}')
            print(f"SUCESS: Saving parquet")
        except ValueError as e:
            print(f"ERROR: Saving parquet - {e}")
    
    def run(self):
        print(f"# START REFINED METHOD")
        for file in self.trusted_data_files:
            self.download_s3_files(file)

        with open(self.config_file_path) as j:
            config_table = json.load(j)

        for table in config_table:
            print(f">>> Creating table {table}")
            try:
                df_origen  = self.read_parquet_file(config_table[table]['origen_file'])
                df_refined = self.create_refined_table(df=df_origen,
                                                    columns=config_table[table]['columns_selected'],
                                                    id_single=config_table[table]['id_single'] 
                                                    )
                self.save_parquet(df=df_refined, file_name=table)
                print(f"SUCESS: Creating {table} table")
            except ValueError as e:
                print(f"ERROR: Creating {table} table - {e}")
        print(f"# FINISH REFINED METHOD")