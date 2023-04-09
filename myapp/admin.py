from django.contrib import admin
from .models import AppUser, Course, Session


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    fieldsets = [
        ('First Name', {'fields': ['first_name']}),
        ('Last Name', {'fields': ['last_name']}),
        ('Email', {'fields': ['email']}),
        ('User Type', {'fields': ['user_role']}),
    ]


class CourseAdmin(admin.ModelAdmin):
    list_display = ('sub_and_cat', 'class_title')


class SessionAdmin(admin.ModelAdmin):
    list_display = ('course', 'description')


admin.site.register(AppUser, UserAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Session, SessionAdmin)