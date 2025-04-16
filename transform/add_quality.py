from utilities.logger import Logger
from datetime import datetime
class ADDQuality:
    def __init__(self):
        self.logger = Logger()

    def add_source_and_date(self, data, source_name):
        data["source"] = source_name
        data["extraction_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.logger.log("   Added source and extraction date to data")
        return data