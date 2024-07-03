import sqlalchemy
import awswrangler as wr

class ConsumeLayer:

    def __init__(self, user, password, host, port, database, s3_refined_path):

        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database
        self.s3_path = s3_refined_path

    def make_connection(self):
        user = self.user 
        password = self.password
        host = self.host
        port = self.port
        database = self.database        
        url = f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}"
        print(f">>> Connecting to {host}:{port} - {database} database")
        
        try:
            conn = sqlalchemy.create_engine(url)
            print(f"SUCESS: Connection true")
        except ValueError as e:
            print(f"ERROR: Connection false")
        
        return conn
    
    def list_parquet_s3_files(self):
        s3_path = self.s3_path
        print(f">>> Listing objects from {s3_path}")
        
        try:
            lista = wr.s3.list_objects(s3_path)
            print(f"SUCESS: Objects list")
        except ValueError as e:
            print(f"ERROR: Objects list - {e}")

        return lista

    def read_s3_parquet(self, file_name):
        s3_uri = self.s3_path
        path = f"{s3_uri}/{file_name}.parquet" 
        print(f">>> Reading {file_name} parquet file from {s3_uri}")
        
        try:
            df = wr.s3.read_parquet(path)
            print(f"SUCESS: File {file_name}.parquet read")
        except ValueError as e:
            print(f"ERROR: File {file_name}.parquet read - {e}")
        
        return df

    def write_table(self, conn, table_name, df):
        print(f">>> Write table {table_name}")
        
        try:
            df.to_sql(name=table_name, con=conn, index=False)
            print(f"SUCESS: Table {table_name} created")
        except ValueError as e:
            print(f"ERROR: Table {table_name} created - {e}")

    def run(self):
        print(f"# START CONSUME METHOD")
        conn = self.make_connection()
        files = self.list_parquet_s3_files()
        for file in files:
            file_name = file.split('/')[-1:][0].split('.parquet')[0]
            df = self.read_s3_parquet(file_name)
            self.write_table(conn, file_name, df)
        print(f"# FINISH CONSUME METHOD")
