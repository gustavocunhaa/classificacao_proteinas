import sqlalchemy
import pandas as pd
from sklearn.preprocessing import minmax_scale

class ReadDatabase():

    def __init__(self, 
                 user, password, host, port, 
                 database, data_query):

        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database
        self.query = data_query

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
        
    def run(self):
        data = self.read_sql(self.make_connection())
        return data
    