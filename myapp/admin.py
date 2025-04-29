from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Syllabus

# 📌 Custom User Admin
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'role', 'is_approved', 'is_staff', 'is_superuser')
    list_filter = ('role', 'is_approved', 'is_staff', 'is_superuser')
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('role', 'is_approved')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Custom Fields', {'fields': ('role', 'is_approved')}),
    )
    search_fields = ('username', 'email')
    ordering = ('username',)

# 📌 Syllabus Admin
class SyllabusAdmin(admin.ModelAdmin):
    list_display = ('course_name', 'department', 'regulation', 'uploaded_by')
    search_fields = ('course_name', 'department', 'regulation')

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Syllabus, SyllabusAdmin)


