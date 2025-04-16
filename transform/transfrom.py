from utilities.logger import Logger
import pandas as pd
from geopy.distance import geodesic

class DataTransformer:
    def __init__(self, df, exchange_rate_df, store_location):
        self.df = df
        self.exchange_rate_df = exchange_rate_df
        self.store_location = store_location
        self.logger = Logger()

    def apply_currency_conversion(self):
        """Merge exchange rates and calculate the local price."""
        # Merge exchange rates and calculate local price
        self.df = self.df.merge(self.exchange_rate_df[['currency', 'rate']], how='left', left_on='currency', right_on='currency')
        self.df['local_price'] = self.df['price'] * self.df['rate']
        self.logger.log("  Merged exchange rates and calculated local price.")
        return self.df

    def calculate_delivery_metrics(self):
        """Calculate late deliveries and late-trip days."""
        # Calculate late deliveries
        self.df['is_late'] = self.df['delivery_date'] > self.df['expected_delivery_date']
        
        # Calculate late-trip days
        self.df['late_trip_days'] = (self.df['delivery_date'] - self.df['expected_delivery_date']).dt.days
        self.df['late_trip_days'] = self.df['late_trip_days'].apply(lambda x: x if x > 0 else 0)  # Only count positive late days
        self.logger.log("  Calculated late deliveries and late-trip days.")
        return self.df

    def determine_locality_flag(self):
        """Flag customers as local or not based on proximity."""
        # Apply proximity check using geodesic distance
        self.df['is_local'] = self.df.apply(lambda row: geodesic((row['latitude'], row['longitude']), self.store_location).km <= 10, axis=1)
        self.logger.log("  Determined locality flag based on proximity.")
        return self.df

    def transform(self):
        """Apply all transformations in sequence."""
        self.df = self.apply_currency_conversion()
        self.df = self.calculate_delivery_metrics()
        self.df = self.determine_locality_flag()
        return self.df
