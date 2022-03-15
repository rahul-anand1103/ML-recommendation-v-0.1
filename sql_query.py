from config import *
import psycopg2
import numpy as np
import pandas as pd
from tqdm import tqdm

class SqlToCsv:  
    def __init__(self,credential) -> None:
        self.credential=credential
    
    def connection(self)->None:
        conn = psycopg2.connect(
            user=self.credential['DATABASE_USERNAME'],
            password=self.credential['DATABASE_PASSWORD'],
            host=self.credential['DATABASE_HOST'],
            port=self.credential['DATABASE_PORT'],
            database=self.credential['DATABASE_NAME']
        )
        self.cursor = conn.cursor()
    
    def sql_query(self,sql_query)->None:
        self.cursor.execute(sql_query)
        self.file_name=sql_query.replace("SELECT * FROM ","").split(" ")[0]+".csv"

    def table_column_name(self)->None:
         self.colnames=[desc[0] for desc in self.cursor.description]
    
    def fetch_data_to_csv(self)->None:
        df = pd.DataFrame(np.array(self.cursor.fetchall()),columns=self.colnames)
        df.to_csv(MAIN_DATA_PATH+self.file_name,index=False)
    

def main():
    sql_to_csv=SqlToCsv(SQL_CREDIENTIAL)
    sql_to_csv.connection()
    for table_name in tqdm(["categories","components_learn_content_detail_informations",
                        "learn_contents","learn_contents__skills","learn_contents__topics",
                        "learn_types","partners","skills","sub_categories","topics"]):
        
        sql_to_csv.sql_query(f"SELECT * FROM {table_name}")
        sql_to_csv.table_column_name()
        sql_to_csv.fetch_data_to_csv()

if __name__ == "__main__":
    main()