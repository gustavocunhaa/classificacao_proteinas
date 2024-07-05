import sqlalchemy
import pandas as pd
from sklearn.preprocessing import minmax_scale

class FeatureProcess():

    def __init__(self, 
                 user, password, host, port, 
                 database, data_query, 
                 min_max = (0, 1)):

        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database
        self.query = data_query
        self.min_max = min_max

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
    
    def read_sql(self, conn):
        query = self.query
        print(f">>> Reading sql: {query}")
            
        try:
            df = pd.read_sql_query(query, conn)
            print(f"SUCESS: Data read")
        except ValueError as e:
            print(f"ERROR: Data read - {e}")

        return df

    def normalize_data(self, feautures: pd.DataFrame):
        min_max = self.min_max
        print(f">>> Normalize data for {min_max} Min Max scale")

        try:
            nomr_data = minmax_scale(feautures, min_max)
            x = pd.DataFrame(nomr_data, columns=feautures.columns.to_list())
            print(f"SUCESS: Normalize Data")
        except ValueError as e:
            print(f"ERROR: Normalize Data - {e}")
        
        return x
        
    def run(self):
        data = self.read_sql(self.make_connection())
        df = self.normalize_data(data.drop(columns=['y']))
        df['y'] = data['y']
        return df
    