import os
import subprocess
import awswrangler as wr


# MAKE RAW COLLECT DATA PROCESS
class RawProcess():

    def __init__(self, kaggle_credentials, kaggle_dataset, raw_folder, s3_raw_folder):
        
        self.kaggle_credentials = kaggle_credentials
        self.kaggle_dataset = kaggle_dataset
        self.raw_folder = raw_folder
        self.s3_raw_path = s3_raw_folder
 
    def download_kaggle_dataset(self, kaggle_credentials, dataset_name, save_path):

        # Utilizando as credenciais para o uso da api
        os.environ['KAGGLE_USERNAME'] = kaggle_credentials['kaggle_user']
        os.environ['KAGGLE_KEY']      = kaggle_credentials['kaggle_password']        

        try:
            subprocess.run(["kaggle", "datasets", "download", "-d", dataset_name, "-p", save_path], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Donwload kaggle dataset error: {e}")

    def save_zip(self, raw_folder, file_name, s3_raw_path):
        file = f"{file_name}.zip"
        path_save = os.path.join(raw_folder, file)
        return wr.s3.upload(local_file=path_save, path=f'{s3_raw_path}/{file}')
    
    def run(self):
        self.download_kaggle_dataset(self.kaggle_credentials, 
                                     self.kaggle_dataset,
                                     self.raw_folder)
        self.save_zip(self.raw_folder, 'protein-data-set', self.s3_raw_path)