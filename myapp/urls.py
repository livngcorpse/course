from django.urls import path
from . import views
from .views import upload, search_syllabus

urlpatterns = [
    # Home Page
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),

    # Books Page
    path('books/', views.books, name='books'),

    # Settings Page
    path('settings/', views.settings, name='settings'),

    # About Page
    path('about/', views.about, name='about'),

    # Feedback Page
    path('feedback/', views.feedback_view, name='feedback'),

    # Syllabus Page
    path('syllabus/', views.syllabus, name='syllabus'),

    # Login Page
    path('login/', views.login_view, name='login'),

    # Signup Page
    path('signup/', views.signup, name='signup'),

    # Profile Page (Login Required)
    path('profile/', views.profile, name='profile'),

    # Faculty Requests Page (Admin Only)
    path('requests/', views.faculty_requests, name='faculty_requests'),


    # Approve Faculty Page (Admin Only)
    path('approve_faculty/<int:faculty_id>/', views.approve_faculty, name='approve_faculty'),

    path('reject_faculty/<int:faculty_id>/', views.reject_faculty, name='reject_faculty'),

    # Upload Syllabus Page (Admin Only)
    path('upload/', views.upload, name='upload'),

    # Logout
    path('logout/', views.logout_view, name='logout'),

    path("search-syllabus/", search_syllabus, name="search_syllabus"),
    
    
    path('superadmin_dashboard/', views.superadmin_dashboard, name='superadmin_dashboard'),
    path('manage_user/<int:user_id>/', views.manage_user_view, name='manage_user'),
    path('approve_faculty/<int:faculty_id>/', views.approve_faculty_view, name='approve_faculty'),
]
