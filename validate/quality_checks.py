from utilities.logger import Logger
import pandas as pd

class DataValidator:
    def __init__(self, df):
        self.df = df
        self.logger = Logger()

    def handle_nulls(self, columns=None, fill_value=0):
        if columns is None:
            self.df.fillna(fill_value, inplace=True)
        else:
            self.df[columns].fillna(fill_value, inplace=True)
        self.logger.log(f"  Handled null values in columns: {columns} with fill value: {fill_value}")
        return self.df

    def remove_duplicates(self):
        before = len(self.df)
        self.df.drop_duplicates(inplace=True)
        after = len(self.df)
        self.logger.log(f"  Removed {before - after} duplicate rows")
        return self.df

    def validate_data(self):
        if 'list_price' in self.df.columns:
            if not pd.api.types.is_numeric_dtype(self.df['list_price']):
                self.df['list_price'] = pd.to_numeric(self.df['list_price'], errors='coerce')

        if 'order_date' in self.df.columns:
            self.df['order_date'] = pd.to_datetime(self.df['order_date'], errors='coerce')
            self.logger.log("  Validated data types and handled errors")
        return self.df