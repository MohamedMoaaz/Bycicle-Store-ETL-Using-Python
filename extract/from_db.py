import pandas as pd
from utilities.logger import Logger

class DatabaseExtractor:
    def __init__(self, db_url):
        self.db_url = db_url
        self.logger = Logger()

    def extract_from_postgres(self, query, engine):
        df = pd.read_sql(query, engine)
        self.logger.log(f"✅ Extracted {len(df)} rows from PostgreSQL")
        return df