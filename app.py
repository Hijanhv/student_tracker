"""
Student Tracker - Streamlit Application
A simple app to track students and their expenses
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from database.data_loader import DataLoader
from services.student_service import StudentService
from utils.statistics import calculate_summary_stats, expenses_by_category
from utils.plots import create_expenses_pie_chart, create_student_expenses_bar_chart, create_expenses_timeline

# Page configuration
st.set_page_config(
    page_title="Student Tracker",
    page_icon="🎓",
    layout="wide"
)

# Initialize services
@st.cache_resource
def init_services():
    data_loader = DataLoader('data')
    student_service = StudentService(data_loader)
    return data_loader, student_service

data_loader, student_service = init_services()

# App title
st.title("🎓 Student Tracker")
st.markdown("Track students and their expenses easily")

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Dashboard", "Students", "Expenses", "Analytics"])

# ========== DASHBOARD PAGE ==========
if page == "Dashboard":
    st.header("📊 Dashboard")
    
    # Load data
    students_df = student_service.get_all_students()
    expenses_df = data_loader.load_expenses()
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Students", len(students_df))
    
    with col2:
        st.metric("Total Expenses", len(expenses_df))
    
    with col3:
        total_amount = expenses_df['amount'].sum() if not expenses_df.empty else 0
        st.metric("Total Amount", f"${total_amount:,.2f}")
    
    with col4:
        avg_amount = expenses_df['amount'].mean() if not expenses_df.empty else 0
        st.metric("Average Expense", f"${avg_amount:,.2f}")
    
    st.markdown("---")
    
    # Recent students
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📋 Recent Students")
        if not students_df.empty:
            st.dataframe(students_df.tail(5), use_container_width=True)
        else:
            st.info("No students yet. Add some in the Students page!")
    
    with col2:
        st.subheader("💰 Recent Expenses")
        if not expenses_df.empty:
            recent_expenses = expenses_df.tail(5)
            # Merge with student names
            recent_with_names = recent_expenses.merge(
                students_df[['student_id', 'name']], 
                on='student_id', 
                how='left'
            )
            st.dataframe(recent_with_names[['name', 'category', 'amount', 'date']], use_container_width=True)
        else:
            st.info("No expenses yet. Add some in the Expenses page!")

# ========== STUDENTS PAGE ==========
elif page == "Students":
    st.header("👥 Student Management")
    
    tab1, tab2 = st.tabs(["View Students", "Add New Student"])
    
    with tab1:
        st.subheader("All Students")
        students_df = student_service.get_all_students()
        
        if not students_df.empty:
            # Search functionality
            search = st.text_input("🔍 Search by name", "")
            if search:
                students_df = students_df[students_df['name'].str.contains(search, case=False)]
            
            st.dataframe(students_df, use_container_width=True)
            
            # Student details
            st.markdown("---")
            st.subheader("Student Details")
            student_names = students_df['name'].tolist()
            selected_student = st.selectbox("Select a student", student_names)
            
            if selected_student:
                student_row = students_df[students_df['name'] == selected_student].iloc[0]
                student_id = student_row['student_id']
                
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**ID:** {student_row['student_id']}")
                    st.write(f"**Name:** {student_row['name']}")
                    st.write(f"**Email:** {student_row['email']}")
                
                with col2:
                    st.write(f"**Phone:** {student_row['phone']}")
                    st.write(f"**Enrollment Date:** {student_row['enrollment_date']}")
                
                # Show student expenses
                st.subheader(f"Expenses for {selected_student}")
                student_expenses = student_service.get_student_expenses(student_id)
                
                if not student_expenses.empty:
                    total = student_expenses['amount'].sum()
                    st.metric("Total Expenses", f"${total:,.2f}")
                    st.dataframe(student_expenses, use_container_width=True)
                else:
                    st.info("No expenses recorded for this student.")
        else:
            st.info("No students in the system. Add your first student!")
    
    with tab2:
        st.subheader("Add New Student")
        
        with st.form("add_student_form"):
            name = st.text_input("Full Name*", placeholder="John Doe")
            email = st.text_input("Email*", placeholder="john.doe@email.com")
            phone = st.text_input("Phone*", placeholder="123-456-7890")
            enrollment_date = st.date_input("Enrollment Date*", value=datetime.now())
            
            submitted = st.form_submit_button("Add Student")
            
            if submitted:
                if name and email and phone:
                    new_id = student_service.add_student(
                        name=name,
                        email=email,
                        phone=phone,
                        enrollment_date=str(enrollment_date)
                    )
                    st.success(f"✅ Student '{name}' added successfully with ID: {new_id}")
                    st.rerun()
                else:
                    st.error("⚠️ Please fill in all required fields.")

# ========== EXPENSES PAGE ==========
elif page == "Expenses":
    st.header("💰 Expense Management")
    
    tab1, tab2 = st.tabs(["View Expenses", "Add New Expense"])
    
    with tab1:
        st.subheader("All Expenses")
        expenses_df = data_loader.load_expenses()
        students_df = student_service.get_all_students()
        
        if not expenses_df.empty:
            # Merge with student names
            expenses_with_names = expenses_df.merge(
                students_df[['student_id', 'name']], 
                on='student_id', 
                how='left'
            )
            
            # Filter options
            col1, col2 = st.columns(2)
            with col1:
                categories = ['All'] + expenses_df['category'].unique().tolist()
                selected_category = st.selectbox("Filter by Category", categories)
            
            with col2:
                student_names = ['All'] + students_df['name'].tolist()
                selected_student = st.selectbox("Filter by Student", student_names)
            
            # Apply filters
            filtered_df = expenses_with_names.copy()
            if selected_category != 'All':
                filtered_df = filtered_df[filtered_df['category'] == selected_category]
            if selected_student != 'All':
                filtered_df = filtered_df[filtered_df['name'] == selected_student]
            
            # Display filtered data
            st.dataframe(filtered_df[['name', 'category', 'amount', 'date', 'description']], use_container_width=True)
            
            # Summary statistics
            st.markdown("---")
            stats = calculate_summary_stats(filtered_df)
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total", f"${stats['total']:,.2f}")
            col2.metric("Average", f"${stats['average']:,.2f}")
            col3.metric("Min", f"${stats['min']:,.2f}")
            col4.metric("Max", f"${stats['max']:,.2f}")
        else:
            st.info("No expenses recorded. Add your first expense!")
    
    with tab2:
        st.subheader("Add New Expense")
        
        students_df = student_service.get_all_students()
        
        if students_df.empty:
            st.warning("⚠️ Please add students first before adding expenses.")
        else:
            with st.form("add_expense_form"):
                student_options = dict(zip(students_df['name'], students_df['student_id']))
                selected_student = st.selectbox("Select Student*", list(student_options.keys()))
                
                category = st.selectbox("Category*", ["Tuition", "Books", "Supplies", "Lab Fees", "Other"])
                amount = st.number_input("Amount ($)*", min_value=0.0, step=0.01, format="%.2f")
                date = st.date_input("Date*", value=datetime.now())
                description = st.text_area("Description", placeholder="Enter expense details...")
                
                submitted = st.form_submit_button("Add Expense")
                
                if submitted:
                    if selected_student and amount > 0:
                        student_id = student_options[selected_student]
                        new_id = student_service.add_expense(
                            student_id=student_id,
                            category=category,
                            amount=amount,
                            date=str(date),
                            description=description
                        )
                        st.success(f"✅ Expense added successfully with ID: {new_id}")
                        st.rerun()
                    else:
                        st.error("⚠️ Please fill in all required fields and ensure amount is greater than 0.")

# ========== ANALYTICS PAGE ==========
elif page == "Analytics":
    st.header("📈 Analytics & Reports")
    
    expenses_df = data_loader.load_expenses()
    students_df = student_service.get_all_students()
    
    if expenses_df.empty:
        st.info("No data available for analytics. Add some expenses first!")
    else:
        # Expenses by Category
        st.subheader("Expenses by Category")
        category_data = expenses_by_category(expenses_df)
        
        col1, col2 = st.columns([2, 1])
        with col1:
            fig = create_expenses_pie_chart(category_data)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.dataframe(category_data, use_container_width=True)
        
        st.markdown("---")
        
        # Expenses by Student
        st.subheader("Total Expenses by Student")
        student_totals = student_service.get_total_expenses_by_student()
        
        if not student_totals.empty:
            col1, col2 = st.columns([2, 1])
            with col1:
                fig = create_student_expenses_bar_chart(student_totals)
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.dataframe(student_totals, use_container_width=True)
        
        st.markdown("---")
        
        # Expenses Timeline
        st.subheader("Expenses Timeline")
        fig = create_expenses_timeline(expenses_df)
        if fig:
            st.plotly_chart(fig, use_container_width=True)

# Footer
st.sidebar.markdown("---")
st.sidebar.info("💡 **Tip:** Use this app to easily track student expenses and generate reports!")
