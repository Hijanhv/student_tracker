"""
Student service for business logic
"""
import pandas as pd
from datetime import datetime

class StudentService:
    def __init__(self, data_loader):
        self.data_loader = data_loader
    
    def get_all_students(self):
        """Get all students"""
        return self.data_loader.load_students()
    
    def get_student_by_id(self, student_id):
        """Get a specific student by ID"""
        df = self.data_loader.load_students()
        student = df[df['student_id'] == student_id]
        return student.iloc[0] if not student.empty else None
    
    def add_student(self, name, email, phone, enrollment_date):
        """Add a new student"""
        df = self.data_loader.load_students()
        new_id = df['student_id'].max() + 1 if not df.empty else 1
        
        new_student = pd.DataFrame([{
            'student_id': new_id,
            'name': name,
            'email': email,
            'phone': phone,
            'enrollment_date': enrollment_date
        }])
        
        df = pd.concat([df, new_student], ignore_index=True)
        self.data_loader.save_students(df)
        return new_id
    
    def get_student_expenses(self, student_id):
        """Get all expenses for a student"""
        expenses_df = self.data_loader.load_expenses()
        return expenses_df[expenses_df['student_id'] == student_id]
    
    def add_expense(self, student_id, category, amount, date, description):
        """Add a new expense"""
        df = self.data_loader.load_expenses()
        new_id = df['expense_id'].max() + 1 if not df.empty else 1
        
        new_expense = pd.DataFrame([{
            'expense_id': new_id,
            'student_id': student_id,
            'category': category,
            'amount': amount,
            'date': date,
            'description': description
        }])
        
        df = pd.concat([df, new_expense], ignore_index=True)
        self.data_loader.save_expenses(df)
        return new_id
    
    def get_total_expenses_by_student(self):
        """Calculate total expenses per student"""
        expenses_df = self.data_loader.load_expenses()
        students_df = self.data_loader.load_students()
        
        if expenses_df.empty:
            return pd.DataFrame()
        
        totals = expenses_df.groupby('student_id')['amount'].sum().reset_index()
        totals.columns = ['student_id', 'total_expenses']
        
        # Merge with student names
        result = totals.merge(students_df[['student_id', 'name']], on='student_id', how='left')
        return result[['name', 'total_expenses']]
