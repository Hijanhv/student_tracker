"""
Data loader for CSV files
"""
import pandas as pd
import os

class DataLoader:
    def __init__(self, data_dir='data'):
        self.data_dir = data_dir
        self.students_file = os.path.join(data_dir, 'students.csv')
        self.expenses_file = os.path.join(data_dir, 'expenses.csv')
    
    def load_students(self):
        """Load students from CSV"""
        try:
            return pd.read_csv(self.students_file)
        except FileNotFoundError:
            return pd.DataFrame(columns=['student_id', 'name', 'email', 'phone', 'enrollment_date'])
    
    def load_expenses(self):
        """Load expenses from CSV"""
        try:
            return pd.read_csv(self.expenses_file)
        except FileNotFoundError:
            return pd.DataFrame(columns=['expense_id', 'student_id', 'category', 'amount', 'date', 'description'])
    
    def save_students(self, df):
        """Save students to CSV"""
        df.to_csv(self.students_file, index=False)
    
    def save_expenses(self, df):
        """Save expenses to CSV"""
        df.to_csv(self.expenses_file, index=False)
