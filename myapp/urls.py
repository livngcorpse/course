from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('books/', views.books, name='books'),
    path('settings/', views.settings, name='settings'),
    path('about/', views.about, name='about'),
    path('feedback/', views.feedback, name='feedback'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('add_syllabus/', views.add_syllabus, name='add_syllabus'),
    path('requests/', views.requests, name='requests'),
    path('upload/', views.upload, name='upload'),
    path('logout/', views.logout_view, name='logout'),
]
