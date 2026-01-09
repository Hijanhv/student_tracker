"""
Statistics utilities
"""
import pandas as pd

def calculate_summary_stats(expenses_df):
    """Calculate summary statistics for expenses"""
    if expenses_df.empty:
        return {
            'total': 0,
            'average': 0,
            'min': 0,
            'max': 0,
            'count': 0
        }
    
    return {
        'total': expenses_df['amount'].sum(),
        'average': expenses_df['amount'].mean(),
        'min': expenses_df['amount'].min(),
        'max': expenses_df['amount'].max(),
        'count': len(expenses_df)
    }

def expenses_by_category(expenses_df):
    """Group expenses by category"""
    if expenses_df.empty:
        return pd.DataFrame()
    
    return expenses_df.groupby('category')['amount'].sum().reset_index()
