"""
Sample data generation utilities for testing and development.

This module provides functions to generate realistic sample data
for testing the Streamlit application without needing live Databricks connections.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Optional, List


def generate_time_series_data(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    freq: str = 'D',
    num_categories: int = 4
) -> pd.DataFrame:
    """
    Generate time series data with multiple metrics.

    Args:
        start_date: Start date for the time series
        end_date: End date for the time series
        freq: Frequency ('D' for daily, 'H' for hourly, 'W' for weekly)
        num_categories: Number of categories to generate

    Returns:
        DataFrame with time series data
    """
    if start_date is None:
        start_date = datetime.now() - timedelta(days=90)
    if end_date is None:
        end_date = datetime.now()

    dates = pd.date_range(start=start_date, end=end_date, freq=freq)
    categories = [f'Category_{i+1}' for i in range(num_categories)]

    data = []
    for date in dates:
        for category in categories:
            # Add some trend and seasonality
            trend = len(data) * 0.5
            seasonal = 100 * np.sin(2 * np.pi * date.dayofyear / 365)
            noise = np.random.normal(0, 50)

            value = 1000 + trend + seasonal + noise

            data.append({
                'date': date,
                'category': category,
                'value': max(0, value),
                'transactions': np.random.randint(50, 500),
                'users': np.random.randint(10, 200)
            })

    return pd.DataFrame(data)


def generate_sales_data(
    num_records: int = 1000,
    num_products: int = 20,
    num_regions: int = 5
) -> pd.DataFrame:
    """
    Generate realistic sales transaction data.

    Args:
        num_records: Number of sales records to generate
        num_products: Number of unique products
        num_regions: Number of regions

    Returns:
        DataFrame with sales data
    """
    np.random.seed(42)

    products = [f'Product_{i+1}' for i in range(num_products)]
    regions = [f'Region_{i+1}' for i in range(num_regions)]
    payment_methods = ['Credit Card', 'Debit Card', 'PayPal', 'Bank Transfer']

    data = {
        'transaction_id': [f'TXN_{i:06d}' for i in range(num_records)],
        'date': [datetime.now() - timedelta(days=np.random.randint(0, 365)) for _ in range(num_records)],
        'product': np.random.choice(products, num_records),
        'region': np.random.choice(regions, num_records),
        'quantity': np.random.randint(1, 10, num_records),
        'unit_price': np.random.uniform(10, 500, num_records),
        'payment_method': np.random.choice(payment_methods, num_records)
    }

    df = pd.DataFrame(data)
    df['total_amount'] = df['quantity'] * df['unit_price']
    df['discount'] = np.random.choice([0, 0.05, 0.10, 0.15, 0.20], num_records, p=[0.5, 0.2, 0.15, 0.1, 0.05])
    df['final_amount'] = df['total_amount'] * (1 - df['discount'])

    return df.sort_values('date', ascending=False).reset_index(drop=True)


def generate_customer_data(num_customers: int = 500) -> pd.DataFrame:
    """
    Generate customer demographic and behavior data.

    Args:
        num_customers: Number of customers to generate

    Returns:
        DataFrame with customer data
    """
    np.random.seed(42)

    segments = ['Premium', 'Standard', 'Basic']
    statuses = ['Active', 'Inactive', 'Churned']
    countries = ['USA', 'UK', 'Germany', 'France', 'Canada', 'Australia', 'Japan']

    data = {
        'customer_id': [f'CUST_{i:05d}' for i in range(num_customers)],
        'signup_date': [datetime.now() - timedelta(days=np.random.randint(0, 730)) for _ in range(num_customers)],
        'segment': np.random.choice(segments, num_customers, p=[0.2, 0.5, 0.3]),
        'status': np.random.choice(statuses, num_customers, p=[0.7, 0.2, 0.1]),
        'country': np.random.choice(countries, num_customers),
        'total_purchases': np.random.randint(1, 100, num_customers),
        'lifetime_value': np.random.uniform(100, 10000, num_customers),
        'average_order_value': np.random.uniform(20, 500, num_customers)
    }

    return pd.DataFrame(data)


def generate_metrics_data(
    num_days: int = 30,
    include_anomalies: bool = False
) -> pd.DataFrame:
    """
    Generate KPI metrics data over time.

    Args:
        num_days: Number of days to generate data for
        include_anomalies: Whether to include anomalous data points

    Returns:
        DataFrame with metrics data
    """
    dates = pd.date_range(start=datetime.now() - timedelta(days=num_days), end=datetime.now(), freq='D')

    data = []
    for i, date in enumerate(dates):
        base_value = 1000
        trend = i * 5
        seasonal = 100 * np.sin(2 * np.pi * i / 7)  # Weekly seasonality
        noise = np.random.normal(0, 50)

        value = base_value + trend + seasonal + noise

        # Add anomalies if requested
        if include_anomalies and np.random.random() < 0.05:
            value *= np.random.choice([0.5, 2.0])  # 50% drop or 200% spike

        data.append({
            'date': date,
            'revenue': max(0, value),
            'orders': int(max(0, value / 50 + np.random.normal(0, 10))),
            'new_customers': int(max(0, 20 + np.random.normal(0, 5))),
            'returning_customers': int(max(0, 50 + np.random.normal(0, 10))),
            'conversion_rate': min(1.0, max(0, 0.03 + np.random.normal(0, 0.005)))
        })

    return pd.DataFrame(data)


def generate_cohort_data(num_cohorts: int = 12) -> pd.DataFrame:
    """
    Generate cohort retention data.

    Args:
        num_cohorts: Number of cohorts (typically months)

    Returns:
        DataFrame with cohort retention data
    """
    cohorts = pd.date_range(start=datetime.now() - timedelta(days=num_cohorts * 30), periods=num_cohorts, freq='MS')

    data = []
    for cohort_date in cohorts:
        cohort_size = np.random.randint(100, 1000)

        for month in range(12):
            # Retention decreases over time with some randomness
            base_retention = 1.0 / (1 + month * 0.3)
            retention = base_retention * np.random.uniform(0.8, 1.2)
            retention = min(1.0, max(0, retention))

            retained_users = int(cohort_size * retention)

            data.append({
                'cohort': cohort_date,
                'month': month,
                'cohort_size': cohort_size,
                'retained_users': retained_users,
                'retention_rate': retention
            })

    return pd.DataFrame(data)
