from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import CustomUser, Syllabus  # Import CustomUser and Syllabus models
from django.core.exceptions import ValidationError

# ✅ User Registration Form
class CustomUserCreationForm(UserCreationForm):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Faculty', 'Faculty'),
        ('Student', 'Student'),
    ]

    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'role']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.role = self.cleaned_data['role']
        if commit:
            user.save()
        return user

# ✅ User Login Form
class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
from django import forms
from .models import Syllabus
from django.contrib.auth import get_user_model

User = get_user_model()

class SyllabusUploadForm(forms.ModelForm):
    class Meta:
        model = Syllabus
        fields = ['course_name', 'department', 'regulation', 'syllabus_file']
        widgets = {
            'course_name': forms.TextInput(attrs={'required': True}),
            'department': forms.Select(attrs={'required': True}),
            'regulation': forms.Select(attrs={'required': True}),
            'syllabus_file': forms.FileInput(attrs={'accept': '.pdf', 'required': True}),
        }

    def __init__(self, *args, **kwargs):
        self._user = kwargs.pop('user', None)  # ✅ Grab user from form init
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        # Get the current user from the form's 'user' attribute
        user = getattr(self, '_user', None)  # Use getattr to avoid errors if _user is not set
        instance = super().save(commit=False)
        if user:
            instance.uploaded_by = user  # Set the uploaded_by field to the user
        if commit:
            instance.save()
        return instance

    # Custom method to set the user when the form is instantiated
    def set_user(self, user):
        self._user = user  # Set the '_user' attribute


class CustomSignupForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']

class CustomLoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'email', 'category', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
