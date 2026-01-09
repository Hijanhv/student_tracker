"""
Student model class
"""

class Student:
    def __init__(self, student_id, name, email, phone, enrollment_date):
        self.student_id = student_id
        self.name = name
        self.email = email
        self.phone = phone
        self.enrollment_date = enrollment_date
    
    def to_dict(self):
        """Convert student object to dictionary"""
        return {
            'student_id': self.student_id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'enrollment_date': self.enrollment_date
        }
    
    def __str__(self):
        return f"{self.name} (ID: {self.student_id})"
