import pandas as pd
from pathlib import Path
from utilities.logger import Logger

class FileExtractor:
    def __init__(self, base_folder):
        self.base_folder = Path(base_folder)
        self.logger = Logger()

    def extract_from_csv(self, department=None, filenames=None):
        if filenames is None:
            filenames = [file.name for file in (self.base_folder / department).glob("*.csv")]
        
        all_data = {}
        for filename in filenames:
            file_path = self.base_folder / department / filename
            df = pd.read_csv(file_path)
            all_data[filename] = df
            self.logger.log(f"✅ Extracted {len(df)} rows from {file_path}")
        return all_data
    


