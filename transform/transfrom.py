from utilities.logger import Logger
import pandas as pd

class DataTransformer:
    def __init__(self):
        self.logger = Logger()

    def apply_currency_conversion(self, products_df, exchange_rate_df):
        egp_rate = exchange_rate_df[exchange_rate_df['currency'] == 'EGP']['rate'].iloc[-1]
        products_df['exchange_rate'] = egp_rate
        products_df['local_price_egp'] = products_df['list_price'] * egp_rate
        return products_df

    def calculate_delivery_metrics(self, stock_df):
        date_cols = ['order_date', 'required_date', 'shipped_date']
        stock_df[date_cols] = stock_df[date_cols].apply(pd.to_datetime, errors='coerce')
        
        stock_df['is_late'] = stock_df['shipped_date'] > stock_df['required_date']
        stock_df['days_late'] = (stock_df['shipped_date'] - stock_df['required_date']).dt.days.clip(lower=0)
        
        stock_df['delivery_status'] = 'Late'
        stock_df.loc[stock_df['shipped_date'] < stock_df['required_date'], 'delivery_status'] = 'Early'
        stock_df.loc[stock_df['shipped_date'] == stock_df['required_date'], 'delivery_status'] = 'On Time'
        return self.df

    def determine_locality_flag(self, customers_df, stores_df):
        store_cities = set(stores_df['city'].str.lower().unique())
        customers_df['is_local'] = customers_df['city'].str.lower().isin(store_cities)
        return customers_df