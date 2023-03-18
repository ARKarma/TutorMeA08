from django.contrib import admin
from .models import User

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    fieldsets = [
        ('First Name', {'fields': ['first_name']}),
        ('Last Name', {'fields': ['last_name']}),
        ('Email', {'fields': ['email']}),
        ('User Type', {'fields': ['user_role']}),
    ]

admin.site.register(User, UserAdmin)