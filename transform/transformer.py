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

    def calculate_delivery_metrics(self, order_items_df):
        date_cols = ['order_date', 'required_date', 'shipped_date']
        order_items_df[date_cols] = order_items_df[date_cols].apply(pd.to_datetime, errors='coerce')
        
        order_items_df['is_late'] = order_items_df['shipped_date'] > order_items_df['required_date']
        order_items_df['days_late'] = (order_items_df['shipped_date'] - order_items_df['required_date']).dt.days.clip(lower=0)
        
        order_items_df['delivery_status'] = 'Late'
        order_items_df.loc[order_items_df['shipped_date'] < order_items_df['required_date'], 'delivery_status'] = 'Early'
        order_items_df.loc[order_items_df['shipped_date'] == order_items_df['required_date'], 'delivery_status'] = 'On Time'
        
        return order_items_df

    def determine_locality_flag(self, customers_df, stores_df, order_items_df):
        orders_with_store_city = order_items_df.merge(
            stores_df[['store_id', 'city']], on='store_id', how='left'
        ).rename(columns={'city': 'store_city'})

        orders_with_both_cities = orders_with_store_city.merge(
            customers_df[['customer_id', 'city']], on='customer_id', how='left'
        ).rename(columns={'city': 'customer_city'})

        orders_with_both_cities['is_local'] = (
            orders_with_both_cities['store_city'].str.lower() ==
            orders_with_both_cities['customer_city'].str.lower()
        )

        customer_locality = orders_with_both_cities.groupby('customer_id')['is_local'].any().reset_index()
        customer_locality['locality'] = customer_locality['is_local'].map({True: 'local', False: 'not_local'})

        result_df = customers_df.merge(customer_locality[['customer_id', 'locality']], on='customer_id', how='left')
        result_df['locality'] = result_df['locality'].fillna('unknown')

        return result_df