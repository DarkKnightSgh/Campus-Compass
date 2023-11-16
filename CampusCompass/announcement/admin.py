from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Announcement

class AnnoncementAdmin(admin.ModelAdmin):
    list_display=[
        'title',
        'content',
        'post_by',
        'list_branch'
    ]

    search_fields=[
        'title',
        'content',
        'post_by',
        'list_branch'
    ]

    list_filter=[
        'branch'
    ]

    def list_branch(self, obj):
        # Retrieve the list of domain tags for the mentor and return them as a string
        branch = obj.branch.all()  # Assuming 'domain' is the name of the TaggableManager field
        return ', '.join(b.branch_name for b in branch)

    list_branch.short_description = "branches"  # Set a custom column header for the domains


admin.site.register(Announcement,AnnoncementAdmin)

