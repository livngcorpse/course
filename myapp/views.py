from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomSignupForm, CustomLoginForm
from .models import CustomUser
from django.contrib.auth.models import User
from .models import Faculty 
from .models import FacultyRequest
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Syllabus
from django.http import JsonResponse

# Home Page View
def home(request):
    return render(request, 'home.html')

# Books Page View
def books(request):
    return render(request, 'books.html')

# Settings Page View
def settings(request):
    return render(request, 'settings.html')

# About Page View
def about(request):
    return render(request, 'about.html')

# Feedback Page View
from django.shortcuts import render, redirect
from .forms import FeedbackForm

def feedback_view(request):
    form = FeedbackForm()
    submitted = False

    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            if request.headers.get('HX-Request'):
                return render(request, 'partials/feedback_success.html')
            return redirect('/feedback?submitted=True')

    if request.GET.get('submitted'):
        submitted = True

    return render(request, 'feedback.html', {'form': form, 'submitted': submitted})


# Syllabus Page View
def syllabus(request):
    context = {
        "regulations": ["R17", "R20", "R23"],
        "departments": ["CSE", "IT", "ECE", "EEE"],
        "years": ["1st Year B.Tech", "2nd Year B.Tech", "3rd Year B.Tech", "4th Year B.Tech"],
    }
    return render(request, "syllabus.html", context)

# Login View
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            # Get the username and password from the form
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            # Authenticate the user
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                # If the user is authenticated, log them in
                login(request, user)
                return redirect('home')  # Redirect to the homepage or dashboard after successful login
            else:
                # If authentication fails, add error
                form.add_error(None, 'Invalid username or password.')
    else:
        form = CustomLoginForm()

    return render(request, 'login.html', {'form': form})

# Signup View
def signup(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomSignupForm()

    return render(request, 'signup.html', {'form': form})

# Profile Page View
@login_required
def profile(request):
    return render(request, 'profile.html')

@login_required
def faculty_requests(request):
    if not request.user.is_admin():
        return redirect('home')

    pending_faculty = CustomUser.objects.filter(role="Faculty", is_active=False)
    return render(request, 'faculty_requests.html', {'pending_faculty': pending_faculty})

# Approve Faculty (Admin Only)
@login_required
def approve_faculty(request, faculty_id):
    if not request.user.is_admin():
        return redirect('home')

    faculty = get_object_or_404(CustomUser, id=faculty_id, role="Faculty", is_active=False)
    
    faculty.is_active = True
    faculty.save()
    
    messages.success(request, f"{faculty.username} has been approved as Faculty.")
    return redirect('faculty_requests')

# Reject Faculty (Admin Only) - NEW FUNCTION
@login_required
def reject_faculty(request, faculty_id):
    if not request.user.is_admin():
        return redirect('home')

    faculty = get_object_or_404(CustomUser, id=faculty_id, role="Faculty", is_active=False)

    # Prevent superadmin from being deleted
    if faculty.is_superuser:
        messages.error(request, "Superadmin cannot be rejected!")
        return redirect('faculty_requests')

    faculty.delete()
    
    messages.success(request, f"Faculty request from {faculty.username} has been rejected.")
    return redirect('faculty_requests')

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SyllabusUploadForm


@login_required
def upload(request):
    if request.method == 'POST':
        form = SyllabusUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.set_user(request.user)
            form.save()
            messages.success(request, "✅ Syllabus uploaded successfully!")
            return redirect('upload')
        else:
            messages.error(request, "❌ Error uploading syllabus. Please check the form.")
    else:
        form = SyllabusUploadForm()
    
    return render(request, 'upload.html', {'form': form})


# Logout View
def logout_view(request):
    logout(request)
    return redirect('login')

def superadmin_dashboard(request):
    if not request.user.is_superuser:
        return redirect('home')  # Redirect non-superadmins to home
    
    users = CustomUser.objects.exclude(username=request.user.username)  # Exclude self
    return render(request, 'superadmin_dashboard.html', {'users': users})

def manage_user_view(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        # Handle the case where the user does not exist
        user = None

    return render(request, 'manage_user.html', {'user': user})

def approve_faculty_view(request, faculty_id):
    # Make sure the block of code inside the function is indented properly
    faculty = get_object_or_404(Faculty, id=faculty_id)

    # Approve the faculty
    faculty.is_approved = True
    faculty.save()

    # Return a response (rendering a template in this case)
    return render(request, 'approve_faculty.html', {'faculty': faculty})

def reject_faculty(request, faculty_id):
    if not request.user.is_admin():
        return redirect('home')

    faculty = get_object_or_404(CustomUser, id=faculty_id)
    faculty.delete()  # Remove faculty request
    messages.info(request, f"{faculty.username} has been rejected.")
    
    return redirect('faculty_requests')

@login_required
def requests_view(request):
    if request.user.role not in ["Admin", "Superadmin"]:  # Allow both roles
        return redirect("home")

    requests = FacultyRequest.objects.all()  # Fetch actual requests
    return render(request, "requests.html", {"requests": requests})


def search_syllabus(request):
    print("✅ search_syllabus view called!")  # Debugging

    regulation = request.GET.get("regulation", "")
    department = request.GET.get("department", "")
    year = request.GET.get("year", "")

    print(f"🔍 Received: regulation={regulation}, department={department}, year={year}")

    syllabi = Syllabus.objects.filter(
        regulation=regulation, department=department, year=year
    )

    if syllabi.exists():
        syllabus_data = [
            {
                "regulation": s.regulation,
                "department": s.department,
                "year": s.year,
                "preview_url": s.preview_url,
                "download_url": s.download_url
            }
            for s in syllabi
        ]
        print("✅ Returning JSON response with data!")
        return JsonResponse({"syllabi": syllabus_data}, safe=False)
    else:
        print("❌ No syllabus found!")
        return JsonResponse({"syllabi": []})
