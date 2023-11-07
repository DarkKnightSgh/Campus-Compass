from django.contrib import admin

from django.shortcuts import render
from django.shortcuts import redirect

from django.contrib import admin
from .models import *

# Register your models here.

class ContactUsAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'query', 'response','closed']
    search_fields = ['name', 'email', 'query']
    list_filter = ['sent_on']
    list_editable=['response','closed']
    readonly_fields = ('name', 'email', 'query', 'sent_on')

    
# Register the ContactUs model with the custom admin class
admin.site.register(ContactUs, ContactUsAdmin)
