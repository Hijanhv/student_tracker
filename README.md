# 🎓 Student Tracker

A beginner-friendly Streamlit application to track students and their expenses.

## 🚀 Live Demo

**[View Live App](https://studenttracker-qjiuacspnn2nrzhbhn8tux.streamlit.app/)**

## Features

- 📊 **Dashboard** - View overview of students and expenses
- 👥 **Student Management** - Add and view student information
- 💰 **Expense Tracking** - Record and manage student expenses
- 📈 **Analytics** - Visualize data with interactive charts

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Local Setup

1. **Clone or download this repository**

2. **Navigate to the project folder**
   ```bash
   cd student_tracker
   ```

3. **Install required packages**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Open your browser**
   - The app will automatically open at `http://localhost:8501`
   - If not, manually navigate to that URL

## Deploy to Streamlit Cloud (Free!)

### Step 1: Prepare Your Code
1. Create a GitHub account if you don't have one
2. Create a new repository on GitHub
3. Upload all your project files to the repository

### Step 2: Deploy on Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click "New app"
4. Select your repository, branch (main), and main file (app.py)
5. Click "Deploy!"

Your app will be live in a few minutes! 🎉

## Project Structure

```
student_tracker/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── data/
│   ├── students.csv      # Student data
│   └── expenses.csv      # Expense data
└── src/
    ├── database/
    │   └── data_loader.py      # CSV data loader
    ├── models/
    │   └── student.py          # Student model
    ├── services/
    │   └── student_service.py  # Business logic
    └── utils/
        ├── file_handler.py     # File utilities
        ├── plots.py            # Chart generation
        └── statistics.py       # Statistical calculations
```

## Usage Guide

### Dashboard Page
- View total number of students and expenses
- See total and average expense amounts
- Quick view of recent students and expenses

### Students Page
- **View Students Tab**: See all students, search by name, view detailed student information
- **Add New Student Tab**: Fill in the form to add a new student

### Expenses Page
- **View Expenses Tab**: See all expenses, filter by category or student
- **Add New Expense Tab**: Record a new expense for any student

### Analytics Page
- View expenses breakdown by category (pie chart)
- Compare total expenses by student (bar chart)
- See expense timeline (scatter plot)

## Data Storage

- Data is stored in CSV files in the `data/` folder
- `students.csv` contains student information
- `expenses.csv` contains expense records
- Data persists between sessions

## Customization

### Adding New Expense Categories
Edit line 239 in [app.py](app.py):
```python
category = st.selectbox("Category*", ["Tuition", "Books", "Supplies", "Lab Fees", "Other", "YOUR_NEW_CATEGORY"])
```

### Changing Colors/Theme
Add a `.streamlit/config.toml` file:
```toml
[theme]
primaryColor = "#FF6B6B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"
```

## Troubleshooting

### Issue: "Module not found"
**Solution**: Make sure you've installed all requirements:
```bash
pip install -r requirements.txt
```

### Issue: "File not found" errors
**Solution**: Make sure you're running the app from the project root directory:
```bash
cd student_tracker
streamlit run app.py
```

### Issue: Data not saving
**Solution**: Check that the `data/` folder exists and has write permissions

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the Streamlit documentation: [docs.streamlit.io](https://docs.streamlit.io)
3. Check Python/Pandas documentation for data-related issues

## License

This project is open source and available for educational purposes.

---

**Made with ❤️ using Streamlit**
