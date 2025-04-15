from sqlalchemy import create_engine

class DatabaseConnector:
    def __init__(self, db_url):
        self.db_url = db_url
        self.engine = None

    def connect(self):
        self.engine = create_engine(self.db_url)
        return self.engine