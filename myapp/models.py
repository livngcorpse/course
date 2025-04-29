from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.core.exceptions import ValidationError

# ✅ Custom User Model
class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('Superadmin', 'Superadmin'),
        ('Admin', 'Admin'),
        ('Faculty', 'Faculty'),
        ('Student', 'Student'),
        ('Pending Faculty', 'Pending Faculty'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Student')
    is_approved = models.BooleanField(default=False)  # For faculty approval system
    is_active = models.BooleanField(default=True)  # For activation control (relevant for faculty)

    def __str__(self):
        return f"{self.username} ({self.role})"

    # Custom methods for checking roles
    def is_superadmin(self):
        return self.role == 'Superadmin'

    def is_admin(self):
        return self.role == 'Admin'

    def is_faculty(self):
        return self.role == 'Faculty'


from django.db import models
from django.conf import settings

class Syllabus(models.Model):
    # Class-level constants for departments and regulations
    DEPARTMENTS = [
        ('CSE', 'Computer Science and Engineering'),
        ('IT', 'Information Technology'),
        ('ECE', 'Electronics and Communication Engineering'),
        ('EEE', 'Electrical and Electronics Engineering'),
        ('MECH', 'Mechanical Engineering'),
        ('CIVIL', 'Civil Engineering'),
    ]

    REGULATIONS = [
        ('R17', 'Regulation 17'),
        ('R20', 'Regulation 20'),
        ('R23', 'Regulation 23'),
    ]

    # Fields
    course_name = models.CharField(max_length=255)
    department = models.CharField(max_length=10, choices=DEPARTMENTS)
    regulation = models.CharField(max_length=10, choices=REGULATIONS)
    syllabus_file = models.FileField(upload_to='syllabi/')
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.course_name} ({self.department}, {self.regulation})"




# ✅ Faculty Model (moved outside Syllabus model)
class Faculty(models.Model):     
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class FacultyRequest(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)  # Replace 'CustomUser' if using another model
    course = models.CharField(max_length=255)
    department = models.CharField(max_length=100)
    is_approved = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Request from {self.user.username} for {self.course}"

from django.db import models

class Feedback(models.Model):
    CATEGORY_CHOICES = [
        ('Suggestion', 'Suggestion'),
        ('Bug Report', 'Bug Report'),
        ('General Inquiry', 'General Inquiry'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.category}"
