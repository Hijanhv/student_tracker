"""
Plotting utilities
"""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def create_expenses_pie_chart(category_data):
    """Create a pie chart for expenses by category"""
    if category_data.empty:
        return None
    
    fig = px.pie(
        category_data, 
        values='amount', 
        names='category',
        title='Expenses by Category',
        hole=0.3
    )
    return fig

def create_student_expenses_bar_chart(student_totals):
    """Create a bar chart for expenses by student"""
    if student_totals.empty:
        return None
    
    fig = px.bar(
        student_totals,
        x='name',
        y='total_expenses',
        title='Total Expenses by Student',
        labels={'total_expenses': 'Total Amount ($)', 'name': 'Student Name'}
    )
    return fig

def create_expenses_timeline(expenses_df):
    """Create a timeline chart for expenses"""
    if expenses_df.empty:
        return None
    
    expenses_df['date'] = pd.to_datetime(expenses_df['date'])
    
    fig = px.scatter(
        expenses_df,
        x='date',
        y='amount',
        color='category',
        size='amount',
        hover_data=['description'],
        title='Expenses Timeline'
    )
    return fig
