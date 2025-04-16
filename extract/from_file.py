import pandas as pd
from pathlib import Path
from utilities.logger import Logger

class FileExtractor:
    def __init__(self, base_folder):
        self.base_folder = Path(base_folder)
        self.logger = Logger()

    def extract_from_csv(self, department, filenames=None):
        department_path = self.base_folder / department
        
        if filenames is None:
            filenames = [file.name for file in department_path.glob("*.csv")]
        
        all_data = {}
        for filename in filenames:
            file_path = department_path / filename
            df = pd.read_csv(file_path)
            all_data[filename] = df
            self.logger.log(f"✅ Extracted {len(df)} rows from {filename} in {department}")
        
        return all_data