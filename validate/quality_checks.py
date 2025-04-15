import pandas as pd

class DataValidator:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def remove_nulls(self, columns: list) -> pd.DataFrame:
        before = len(self.df)
        self.df = self.df.dropna(subset=columns)
        after = len(self.df)
        print(f"🧹 Removed {before - after} rows with nulls in {columns}")
        return self.df

    def remove_duplicates(self) -> pd.DataFrame:
        before = len(self.df)
        self.df = self.df.drop_duplicates()
        after = len(self.df)
        print(f"♻️ Removed {before - after} duplicate rows")
        return self.df

    def validate_numeric_range(self, column: str, min_val: float = 0) -> pd.DataFrame:
        before = len(self.df)
        self.df = self.df[self.df[column] >= min_val]
        after = len(self.df)
        print(f"✅ Removed {before - after} rows where {column} < {min_val}")
        return self.df