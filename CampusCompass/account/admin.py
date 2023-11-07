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


class MentorAdmin(admin.ModelAdmin):
    list_display=(
        'student',
        'username',
        'approved',
        'resume',
        'list_domains',
    )
    search_fields=[
        'student',
        'username',
        'approved',
        'domain'
    ]
    list_editable= [
        'approved'
    ]
    list_filter=[
        'domain',
        'approved',
        
    ]

    def list_domains(self, obj):
        # Retrieve the list of domain tags for the mentor and return them as a string
        domain_tags = obj.domain.all()  # Assuming 'domain' is the name of the TaggableManager field
        return ', '.join(tag.name for tag in domain_tags)

    list_domains.short_description = "Domains"  # Set a custom column header for the domains


admin.site.register(Student,StudentAdmin)
admin.site.register(Mentor,MentorAdmin)