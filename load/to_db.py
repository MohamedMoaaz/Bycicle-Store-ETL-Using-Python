from utilities.logger import Logger
class DataBaseLoader:
    def __init__(self, engine):
        self.engine = engine
        self.logger = Logger()
        

    def load_to_postgres(self, df, table_name, if_exists="replace", index=False):
        df.to_sql(table_name, con=self.engine, if_exists=if_exists, index=index)
        self.logger.log(f"  Loaded {len(df)} rows into {table_name} in PostgreSQL")
