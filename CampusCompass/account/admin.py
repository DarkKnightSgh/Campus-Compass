from django.contrib import admin

# Register your models here.
from .models import *
from taggit.models import Tag 

class StudentAdmin(admin.ModelAdmin):
    list_display=(
        'student_id',
        'user',
        'department',
        'branch',
        'college_email',
        'is_mentor',
        'year_of_passing_out',
    )
    search_fields=[
        'department',
        'branch',
        'student_id',
        'user',
        'college_email',
        'whatsapp_number',

    ]
    list_editable= [
        "is_mentor",
    ]
    list_filter=[
        'department',
        'is_mentor',
        'email_confirmed',
        'show_number',
        'year_of_passing_out',
        
    ]
    # readonly_fields = (
    #     'student_id',
    #     'whatsapp_number',
    #     'whatsapp_link',
    #     'user',
    #     'department',
    #     'branch',
    #     'college_email',
    #     'show_number',
    #     'email_confirmed',
    #     'year_of_passing_out',
    # ) 
