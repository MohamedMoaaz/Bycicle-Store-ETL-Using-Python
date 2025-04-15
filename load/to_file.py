from utilities.logger import Logger
from pathlib import Path

class FileLoader:
    def __init__(self, folder_path):
        self.folder_path = Path(folder_path)
        self.logger = Logger()

    def load_to_csv(self, df, file_name):
        file_path = self.folder_path / file_name  
        df.to_csv(file_path, index=False)
        self.logger.log(f"✅ Loaded {len(df)} rows into {file_name} in CSV format")